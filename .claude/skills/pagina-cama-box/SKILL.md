---
name: pagina-cama-box
description: "Gera a página HTML de descrição (Simplo7) de uma cama box (colchão + base) a partir do colchão avulso já cadastrado no catálogo. Busca as fotos certas no bucket Supabase (colchão/cama box montada e base separada por cor), aplica o padrão de box (blindado, marca, garantia, pés) e monta as 8 seções do layout padrão. Use quando o usuário pedir 'cama box de <produto>', 'monta a página da cama box', 'faz o HTML da cama box do <produto>', ou /pagina-cama-box."
---

# Página de Cama Box (Simplo7)

Gera a versão "cama box" (colchão + base) de um produto que já tem página de colchão avulso no catálogo, reaproveitando dados e trocando/adicionando as fotos certas de base.

## Dependências

- **Fluxo geral, organização e SEO:** ler `../pagina-produto-simplo7/SKILL.md` e aplicar todas as regras, inclusive a entrega obrigatória de Meta Title, Meta Description, H1 e Meta Keywords.
- **Estrutura do layout:** seguir o padrão do arquivo de referência `saidas/mockup-produto-livorno-v2.html` e de qualquer `descricao-simplo7-*-conjunto.html` já existente (ex: `saidas/produtos/tower/queen/conjunto/`).
- **Dados do colchão:** a página de colchão avulso do mesmo produto, se existir (`saidas/produtos/**/colchao/descricao-simplo7-*.html`) — é a fonte mais confiável pra espuma/densidade, conforto, suporte de peso, tecido e medidas
- **Credenciais do bucket:** `.env` → `SUPABASE_URL`, `SUPABASE_ANON_KEY` (ou `SUPABASE_SERVICE_KEY`), `SUPABASE_BUCKET`, `SUPABASE_BUCKET_FOLDER`, `SUPABASE_STORAGE_URL`

---

## Onde estão as fotos (bucket `catalogo`, pasta `products/`)

O bucket tem duas famílias de pastas relevantes pra montar uma cama box:

### 1. Fotos do colchão e da cama box montada
Pasta por produto: `products/<categoria>-<produto>/` (ex: `espuma-d20-comfortopedic`, `mola-tower`).

Dentro dela, por tamanho, os arquivos seguem o padrão:
- `colchao-<produto>-<tamanho>.jpg` — colchão isolado, foto de estúdio
- `colchao-<produto>-<tamanho>-cena.jpg` — colchão isolado, foto de ambiente (**preferir sempre que existir**)
- `cama-box-<produto>-<tamanho>.jpg` — colchão + base montados, foto de estúdio
- `cama-box-<produto>-<tamanho>-cena.jpg` — colchão + base montados, foto de ambiente
- `tecido-<produto>.jpg` — close do tecido (uso opcional)

Nem todo tamanho tem versão "-cena". Se faltar a cena do tamanho exato (ex: não existe `colchao-d20-comfortopedic-solteiro-cena.jpg`), usar a cena de outro tamanho do mesmo produto como fallback (ex: a versão `-casal-cena.jpg`) e avisar o usuário que foi um fallback — não deixar de usar cena por causa disso, cena sempre fica melhor que foto de estúdio.

### 2. Fotos da base/box separada, por cor
Pasta por linha + cor: `products/box-suede-<cor>/` (box normal) ou `products/box-bau-suede-<cor>/` (box baú).

Cores disponíveis: `bege`, `cinza`, `marrom`, `preto`.

Dentro de cada pasta de cor, por tamanho:
- `box-suede-<cor>-<tamanho>.jpg` — base isolada, foto de estúdio (usar nas medidas)
- `box-suede-<cor>-<tamanho>-cena.jpg` — base isolada, foto de ambiente (usar na seção Base Box)

Nem toda cor tem todos os tamanhos — conferir antes de montar a URL.

### Como listar o conteúdo de uma pasta do bucket

Não existe `find`/`ls` num bucket remoto — listar via API do Supabase Storage (não precisa Python, o projeto não tem; usar Node puro lendo o `.env` na mão):

```bash
node -e "
const fs = require('fs');
const env = {};
fs.readFileSync('.env', 'utf8').split('\n').forEach(line => {
  const m = line.match(/^([A-Z_]+)=(.*)$/);
  if (m) env[m[1]] = m[2].trim();
});
const url = env.SUPABASE_URL;
const key = env.SUPABASE_SERVICE_KEY || env.SUPABASE_ANON_KEY;
const bucket = env.SUPABASE_BUCKET;
const folder = env.SUPABASE_BUCKET_FOLDER;
fetch(url + '/storage/v1/object/list/' + bucket, {
  method: 'POST',
  headers: {apikey: key, Authorization: 'Bearer ' + key, 'Content-Type': 'application/json'},
  body: JSON.stringify({prefix: folder + '/<PASTA>/', limit: 100})
}).then(r => r.json()).then(d => console.log(d.map(x => x.name).join('\n')));
"
```

Trocar `<PASTA>` por `espuma-d20-comfortopedic`, `box-suede-preto`, etc. Pra ver a lista de pastas que existem, rodar com `prefix: folder + '/'`.

A URL pública final segue sempre este formato:
```
https://supabase.senhorcolchao.com/storage/v1/object/public/catalogo/products/<pasta>/<arquivo>.jpg
```

**Sempre validar a URL com `curl -s -o /dev/null -w "%{http_code}"` antes de colocar no HTML** — não presumir o nome do arquivo, listar e confirmar.

---

## Padrão de box (aplicar sempre, é fixo no catálogo)

- **Box blindado** — fechado lateralmente em MDF. Mencionar isso na seção de benefícios e na seção Base Box (não é opcional, é diferencial do produto).
- **Estrutura:** madeira de eucalipto (reflorestamento), com reforços internos.
- **Revestimento:** suede na cor escolhida + tampo antiderrapante.
- **Tratamento:** anticupim e antimofo na base; antiácaro/antibactéria no colchão (se a linha do colchão já mencionar isso).
- **Pés:** solteiro leva **6 pés em madeira**; casal e queen levam **7 pés em madeira (2 com rodízio)** — se for um tamanho ainda não confirmado (king, queen conjugada etc.), perguntar antes de assumir.
- **Altura da base:** 40 cm é o padrão observado no catálogo (pés de 12 cm inclusos). Altura final do conjunto = altura do colchão + 40 cm.
- **Garantia:** 90 dias, salvo o usuário informar outro valor pro produto específico.

### Marca — não presumir

O campo "Marca" da página do Simplo7 nem sempre bate com a marca real informada pelo usuário (já aconteceu de constar "Herval" no site sendo que o produto é **Orthoflex**). Sempre que a marca não estiver 100% confirmada pelo usuário na conversa, perguntar antes de publicar — não copiar cegamente o que aparece no site.

### Texto de benefício "custo-benefício"

Manter genérico — **não citar o nome de uma linha/tecnologia específica** (ex: não escrever "qualidade Comfortopedic"). Usar algo como "Opção acessível com qualidade." e deixar o resto do texto focado em entrega/montagem grátis.

---

## Workflow

1. **Confirmar com o usuário:** produto (nome/densidade), tamanho (solteiro/casal/queen/...), cor da base, e marca (se não tiver certeza).
2. **Levantar dados do colchão** — ler a página de colchão avulso já existente do mesmo produto/tamanho (`saidas/produtos/**/colchao/`). Se não existir, extrair da página real do produto no site (`WebFetch` na URL do Simplo7) ou pedir os dados ao usuário. Nunca inventar densidade, suporte de peso ou medidas.
3. **Listar as pastas do bucket** (`espuma-<produto>` ou `mola-<produto>`, e `box-suede-<cor>`) e confirmar os nomes exatos dos arquivos antes de montar as URLs.
4. **Montar o HTML** nas 8 seções do padrão (Hero → Benefícios → Colchão → Base Box → Ficha técnica → Medidas → Aviso de entrega → CTA), usando o CSS já definido (`--s7-blue #001da4`, `--s7-yellow #f7cf00`, etc. — ver memória `pagina-produto-simplo7`).
   - Hero: foto de cena da cama box montada (`cama-box-<produto>-<tamanho>-cena.jpg`).
   - Seção Colchão: foto de cena do colchão (com fallback de tamanho se precisar).
   - Seção Base Box: foto de cena da base na cor pedida (`box-suede-<cor>-<tamanho>-cena.jpg`).
   - Medidas: fotos de estúdio (colchão e base) + altura/largura/comprimento de cada peça.
   - Aplicar o padrão de box (blindado, pés, garantia) e a marca confirmada.
5. **Salvar em** `saidas/produtos/<categoria>/<produto>/<tamanho>/cama-box/descricao-simplo7-<produto>-<tamanho>-cama-box.html`
6. **Validar as imagens** com `curl` antes de entregar.
7. **Gerar o bloco de SEO obrigatório** conforme `../pagina-produto-simplo7/SKILL.md`, adaptado para cama box: Meta Title, Meta Description, Tag H1 e Meta Keywords em branco.
8. **Alinhar com Google Ads** quando houver termos de busca reais relevantes, sem repetir keywords artificialmente e usando URL final sem `www`.
9. Avisar qualquer fallback usado (ex: foto de cena de outro tamanho, ausência de foto isolada da base) pra o usuário saber que pode trocar depois se tiver material melhor.
