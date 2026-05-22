#!/usr/bin/env node
/**
 * Gerador de imagens via OpenRouter
 * Uso: node scripts/gerar-imagem.js "prompt em inglês" "caminho/saida.png" [modelo]
 *
 * Modelos disponíveis:
 *   gpt4o   → openai/gpt-4o (padrão — melhor qualidade, lançamentos e produtos)
 *   gemini  → google/gemini-2.0-flash-exp:free (rápido, stories e peças secundárias)
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

function loadEnv() {
  const envPath = path.join(__dirname, '..', '.env');
  if (!fs.existsSync(envPath)) return;
  fs.readFileSync(envPath, 'utf8').split('\n').forEach(line => {
    line = line.trim();
    if (!line || line.startsWith('#') || !line.includes('=')) return;
    const [key, ...rest] = line.split('=');
    if (!(key.trim() in process.env)) process.env[key.trim()] = rest.join('=').trim();
  });
}

loadEnv();

const MODELS = {
  // GPT Image — melhor qualidade (lançamentos, produto principal, D-Day)
  pro:    'openai/gpt-5-image',
  // GPT Image Mini — mais barato, boa qualidade
  mini:   'openai/gpt-5-image-mini',
  // Gemini Flash Image — rápido (stories, peças secundárias)
  fast:   'google/gemini-2.5-flash-image',
  // Aliases
  gpt4o:  'openai/gpt-5-image',
  gemini: 'google/gemini-2.5-flash-image',
};

async function gerarImagem(prompt, outputPath, modelAlias = 'gpt4o') {
  const key = process.env.AI_IMG_CREATOR_OPENROUTER_KEY;
  if (!key) throw new Error('AI_IMG_CREATOR_OPENROUTER_KEY não encontrada no .env');

  const model = MODELS[modelAlias] || modelAlias;
  console.log(`Modelo: ${model}`);
  console.log(`Prompt: ${prompt}`);

  const body = JSON.stringify({
    model,
    messages: [{ role: 'user', content: prompt }],
  });

  return new Promise((resolve, reject) => {
    const req = https.request({
      hostname: 'openrouter.ai',
      path: '/api/v1/chat/completions',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${key}`,
        'HTTP-Referer': 'https://senhorcolchao.com.br',
        'X-Title': 'Senhor Colchao MazyOS',
      },
    }, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (json.error) return reject(new Error(JSON.stringify(json.error)));

          const msg = json.choices?.[0]?.message;

          // 1. Campo images[] (OpenRouter GPT-5-image / Gemini image)
          const images = msg?.images;
          if (Array.isArray(images) && images.length > 0) {
            const imgUrl = images[0]?.image_url?.url || images[0]?.url || '';
            if (imgUrl.startsWith('data:image')) {
              const b64 = imgUrl.split(',')[1];
              fs.mkdirSync(path.dirname(outputPath), { recursive: true });
              fs.writeFileSync(outputPath, Buffer.from(b64, 'base64'));
              resolve(outputPath);
              return;
            }
            if (imgUrl.startsWith('http')) {
              baixarImagem(imgUrl, outputPath).then(resolve).catch(reject);
              return;
            }
          }

          // 2. Fallback: URL ou base64 no content textual
          const content = msg?.content || '';
          const urlMatch = (content || '').match(/https?:\/\/[^\s)"']+\.(?:png|jpg|jpeg|webp)/i);
          if (urlMatch) {
            baixarImagem(urlMatch[0], outputPath).then(resolve).catch(reject);
            return;
          }
          const b64Match = (content || '').match(/data:image\/[^;]+;base64,([A-Za-z0-9+/=]+)/);
          if (b64Match) {
            fs.mkdirSync(path.dirname(outputPath), { recursive: true });
            fs.writeFileSync(outputPath, Buffer.from(b64Match[1], 'base64'));
            resolve(outputPath);
            return;
          }

          console.log('Resposta bruta:', JSON.stringify(msg)?.slice(0, 500));
          reject(new Error('Nenhuma imagem encontrada na resposta.'));
        } catch (e) {
          reject(new Error(`Erro ao parsear resposta: ${e.message}\nRaw: ${data.slice(0, 300)}`));
        }
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

function baixarImagem(url, outputPath) {
  return new Promise((resolve, reject) => {
    fs.mkdirSync(path.dirname(outputPath), { recursive: true });
    const file = fs.createWriteStream(outputPath);
    https.get(url, res => {
      if (res.statusCode === 301 || res.statusCode === 302) {
        file.close();
        baixarImagem(res.headers.location, outputPath).then(resolve).catch(reject);
        return;
      }
      res.pipe(file);
      file.on('finish', () => { file.close(); resolve(outputPath); });
    }).on('error', e => { fs.unlink(outputPath, () => {}); reject(e); });
  });
}

// CLI
const [,, prompt, outputPath, modelo] = process.argv;
if (!prompt || !outputPath) {
  console.error('Uso: node scripts/gerar-imagem.js "prompt" "saida.png" [gpt4o|gemini]');
  process.exit(1);
}

gerarImagem(prompt, outputPath, modelo || 'gpt4o')
  .then(p => console.log(`\nImagem salva em: ${p}`))
  .catch(e => { console.error('Erro:', e.message); process.exit(1); });
