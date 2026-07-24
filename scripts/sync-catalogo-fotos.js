#!/usr/bin/env node
// Sincroniza (nas duas direções) a pasta local `catalogo-fotos/` com o bucket Supabase `catalogo`.
// Uso: node scripts/sync-catalogo-fotos.js
//
// A cada execução:
//   1. Empurra pro bucket qualquer foto local nova ou alterada desde a última sincronização
//      (protege edição local: roda antes de puxar, pra não sobrescrever o que você acabou de adicionar).
//   2. Puxa do bucket qualquer foto nova ou alterada lá (comparando com o manifesto local).
//
// Nunca deleta nada, nem local nem no bucket — só adiciona/atualiza. Ignora arquivos de sistema
// (.DS_Store) e o próprio manifesto (.sync-manifest.json).

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const DEST = path.join(ROOT, 'catalogo-fotos');
const MANIFEST_PATH = path.join(DEST, '.sync-manifest.json');
const IGNORE = new Set(['.DS_Store', '.sync-manifest.json']);

const env = {};
fs.readFileSync(path.join(ROOT, '.env'), 'utf8').split('\n').forEach(line => {
  const m = line.match(/^([A-Z_]+)=(.*)$/);
  if (m) env[m[1]] = m[2].trim();
});

const SUPABASE_URL = env.SUPABASE_URL;
const KEY = env.SUPABASE_SERVICE_KEY || env.SUPABASE_ANON_KEY;
const BUCKET = env.SUPABASE_BUCKET;
const FOLDER = env.SUPABASE_BUCKET_FOLDER;

if (!SUPABASE_URL || !KEY || !BUCKET || !FOLDER) {
  console.error('Faltam variáveis SUPABASE_* no .env (SUPABASE_URL, SUPABASE_SERVICE_KEY/SUPABASE_ANON_KEY, SUPABASE_BUCKET, SUPABASE_BUCKET_FOLDER).');
  process.exit(1);
}
if (!env.SUPABASE_SERVICE_KEY) {
  console.error('Aviso: usando SUPABASE_ANON_KEY — upload provavelmente vai falhar (anon não tem permissão de escrita). Adicione SUPABASE_SERVICE_KEY no .env.');
}

function extOf(name) { return path.extname(name).toLowerCase(); }
const CONTENT_TYPES = { '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp' };

async function listPrefix(prefix) {
  const r = await fetch(`${SUPABASE_URL}/storage/v1/object/list/${BUCKET}`, {
    method: 'POST',
    headers: { apikey: KEY, Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ prefix, limit: 1000 }),
  });
  if (!r.ok) throw new Error(`Falha ao listar ${prefix}: ${r.status}`);
  return r.json();
}

async function listAllBucketFiles() {
  const root = await listPrefix(`${FOLDER}/`);
  const dirs = root.filter(x => x.id === null).map(x => x.name);
  const rootFiles = root
    .filter(x => x.id !== null)
    .map(x => ({ path: `${FOLDER}/${x.name}`, updated_at: x.updated_at, size: x.metadata?.size }));

  let all = [...rootFiles];
  for (const d of dirs) {
    const items = await listPrefix(`${FOLDER}/${d}/`);
    for (const it of items) {
      if (it.id !== null) {
        all.push({ path: `${FOLDER}/${d}/${it.name}`, updated_at: it.updated_at, size: it.metadata?.size });
      }
    }
  }
  return all;
}

function listAllLocalFiles() {
  const out = [];
  function walk(dir) {
    for (const name of fs.readdirSync(dir)) {
      if (IGNORE.has(name)) continue;
      const full = path.join(dir, name);
      const stat = fs.statSync(full);
      if (stat.isDirectory()) walk(full);
      else out.push(full);
    }
  }
  if (fs.existsSync(DEST)) walk(DEST);
  return out;
}

function loadManifest() {
  if (fs.existsSync(MANIFEST_PATH)) return JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf8'));
  return {};
}
function saveManifest(m) {
  fs.writeFileSync(MANIFEST_PATH, JSON.stringify(m, null, 2));
}

function localPathFor(bucketPath) {
  const rel = bucketPath.startsWith(`${FOLDER}/`) ? bucketPath.slice(FOLDER.length + 1) : bucketPath;
  return path.join(DEST, rel);
}
function bucketPathFor(localFile) {
  const rel = path.relative(DEST, localFile).split(path.sep).join('/');
  return `${FOLDER}/${rel}`;
}

(async () => {
  fs.mkdirSync(DEST, { recursive: true });
  const manifest = loadManifest();

  // Migração: manifesto de versões antigas do script não tinha localMtimeMs.
  // Preenche a partir do arquivo atual (assume que já estava sincronizado) em vez de
  // marcar tudo como "alterado" e reenviar 340 arquivos à toa na primeira rodada.
  for (const [bucketPath, entry] of Object.entries(manifest)) {
    if (entry.localMtimeMs == null) {
      const localPath = localPathFor(bucketPath);
      if (fs.existsSync(localPath)) entry.localMtimeMs = fs.statSync(localPath).mtimeMs;
    }
  }

  // --- 1. EMPURRAR: arquivos locais novos ou alterados desde a última sincronização ---
  const localFiles = listAllLocalFiles();
  let pushed = 0, pushFailed = 0;
  const justPushed = new Set();

  for (const localFile of localFiles) {
    const bucketPath = bucketPathFor(localFile);
    const stat = fs.statSync(localFile);
    const prev = manifest[bucketPath];
    const localChanged = !prev || prev.localMtimeMs !== stat.mtimeMs;

    if (!localChanged) continue;

    const ct = CONTENT_TYPES[extOf(localFile)] || 'application/octet-stream';
    try {
      const buf = fs.readFileSync(localFile);
      const r = await fetch(`${SUPABASE_URL}/storage/v1/object/${BUCKET}/${bucketPath}`, {
        method: 'POST',
        headers: { apikey: KEY, Authorization: `Bearer ${KEY}`, 'Content-Type': ct, 'x-upsert': 'true' },
        body: buf,
      });
      if (!r.ok) throw new Error(`HTTP ${r.status}: ${await r.text()}`);
      manifest[bucketPath] = { updated_at: new Date().toISOString(), size: stat.size, localMtimeMs: stat.mtimeMs };
      justPushed.add(bucketPath);
      console.log('ENVIADO:', bucketPath);
      pushed++;
    } catch (e) {
      console.error('FALHOU (envio):', bucketPath, e.message);
      pushFailed++;
    }
  }
  saveManifest(manifest); // salva progresso antes da fase de download

  // --- 2. PUXAR: arquivos novos ou alterados no bucket ---
  const bucketFiles = await listAllBucketFiles();
  let downloaded = 0, skipped = 0, pullFailed = 0;

  for (const f of bucketFiles) {
    if (justPushed.has(f.path)) { skipped++; continue; }
    const localPath = localPathFor(f.path);
    const prev = manifest[f.path];
    const unchanged = prev && prev.updated_at === f.updated_at && fs.existsSync(localPath);

    if (unchanged) { skipped++; continue; }

    try {
      const publicUrl = `${SUPABASE_URL}/storage/v1/object/public/${BUCKET}/${f.path}`;
      const r = await fetch(publicUrl);
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const buf = Buffer.from(await r.arrayBuffer());
      fs.mkdirSync(path.dirname(localPath), { recursive: true });
      fs.writeFileSync(localPath, buf);
      const stat = fs.statSync(localPath);
      manifest[f.path] = { updated_at: f.updated_at, size: f.size, localMtimeMs: stat.mtimeMs };
      downloaded++;
    } catch (e) {
      console.error('FALHOU (download):', f.path, e.message);
      pullFailed++;
    }
  }

  saveManifest(manifest);

  console.log(`\nSincronização concluída.`);
  console.log(`  enviados pro bucket: ${pushed}${pushFailed ? ` (falharam: ${pushFailed})` : ''}`);
  console.log(`  baixados/atualizados: ${downloaded}`);
  console.log(`  sem mudança (pulados): ${skipped}${pullFailed ? ` (falharam: ${pullFailed})` : ''}`);
  console.log(`  pasta local: ${DEST}`);
})();
