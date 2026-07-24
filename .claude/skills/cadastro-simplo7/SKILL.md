---
name: cadastro-simplo7
description: "Cadastra ou corrige produto ao vivo na Simplo7 via API: busca SKU, custo e preço de venda no catálogo do Campaign Manager (nunca no Bling direto, evita produto dessincronizado), monta o JSON de criação com a combinação (variação) certa pro tipo de produto — colchão avulso, cama box com colchão ou cama box sem colchão — e cria via POST /ws/wsprodutos.json. Use quando o usuário pedir para subir produto na Simplo7, criar variação, corrigir combinação errada, ou perguntar SKU/preço/custo de um produto."
---

# Cadastro de Produto na Simplo7

Cobre o fluxo operacional de colocar um produto ao vivo na Simplo7: de onde vêm os dados comerciais (SKU/custo/preço), como montar o HTML de descrição na skill certa pro tipo de produto, e como montar o JSON de `WsprodutoEstoque` com a combinação (variação) certa.

## Passo 0 — Escolher a skill certa pra montar o HTML antes de criar

**Nunca escrever o HTML de descrição direto nesta skill.** Ela cuida só do cadastro (dados comerciais + JSON da API); quem manda no conteúdo/estrutura da página é:

- **Produto único** (colchão avulso, box avulso, box baú, bicama — sem colchão+base juntos): seguir `../pagina-produto-simplo7/SKILL.md`. Layout de 6 seções (Hero → Benefícios → Composição → Ficha técnica → Medidas → CTA), **1 foto só no Hero** (a mesma foto não repete na seção de composição).
- **Conjunto cama box** (colchão + base juntos, um produto só): seguir `../pagina-cama-box/SKILL.md`. Layout de 8 seções, com **3 fotos de cena diferentes** — Hero (conjunto montado), seção Colchão (colchão isolado) e seção Base Box (base isolada na cor certa) — mais fotos de estúdio na seção Medidas. **Isso não é foto repetida**, são arquivos diferentes; não aplicar aqui o ajuste "1 foto só no Hero" do produto único — foi minha confusão de uma vez (ver Passo 5).

Se não tiver certeza se o produto é "único" ou "conjunto", perguntar antes de montar o HTML — a estrutura de seções e a contagem de fotos esperada são diferentes.

## Passo 1 — Buscar SKU, custo e preço no Campaign Manager (nunca direto no Bling)

O Campaign Manager (`https://messenger.senhorcolchao.com`) é o catálogo comercial de referência. É lá que o usuário sincroniza SKU/preço/estoque de verdade — usar essa fonte evita que a Simplo7 fique com números diferentes do Bling.

Front-end pra navegar visualmente (não dá pra buscar dado direto de lá, é SPA React): `https://messenger.senhorcolchao.com/products`.

API (dado real, use sempre esta):

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
curl -s \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  "$BASE_URL/api/products/admin"
```

Credenciais `CAMPAIGN_MANAGER_URL` e `CAMPAIGN_MANAGER_TOKEN` estão no `.env` da raiz do projeto `senhor-colchao` (não confundir com `SIMPLO7_APP_KEY`, que fica no `.env` da raiz do projeto **Campaign Manager**, projeto irmão).

Usar `/api/products/admin` (não `/api/products` puro) — só o `/admin` traz `costPrice`/`publishedCostPrice` (custo) e `supplier` (fornecedor). O endpoint público omite esses campos de propósito.

Cada item retornado é um **modelo** de produto com uma lista de **variantes**:

```json
{
  "name": "Bicama em Molas",
  "brand": "Fa Colchões",
  "category": "Bicama",
  "variants": [
    {
      "skuId": "101410",
      "size": "88x188",
      "color": "Prime Cinza",
      "tablePrice": 2549.9,
      "installmentPrice": 2039.9,
      "costPrice": "1020",
      "publishedCostPrice": "1019.98",
      "supplier": "Fa Colchões",
      "tipo": "Molas Ensacadas",
      "conforto": "Intermediário",
      "pesoSuportado": "Até 100kg",
      "altura": 38,
      "stock": 0,
      "imageUrl": "https://supabase.senhorcolchao.com/storage/v1/object/public/catalogo/products/..."
    }
  ]
}
```

Mapeamento pro cadastro Simplo7:

| Campo Campaign Manager | Campo Simplo7 |
|---|---|
| `skuId` | `Wsproduto.sku` / `WsprodutoEstoque.sku` |
| `tablePrice` | `WsprodutoEstoque.valor_venda` |
| `costPrice` ou `publishedCostPrice` | `WsprodutoEstoque.valor_compra` (campo existe, mas historicamente não vinha sendo preenchido — preencher a partir de agora) |
| `size` | `WsprodutoEstoque.largura` / `.comprimento` + atributo do grupo 48 |
| `altura` | `WsprodutoEstoque.altura` |
| `color` | nome do produto + atributo de cor, se a categoria tiver combinação de cor |
| `brand` | confirmar `marca_id` certo via `GET /ws/wsmarcas.json` (marca pode ter nome levemente diferente) |
| `installmentPrice` | preço à vista/promocional — **não** usar automaticamente como `valor_promocao`; só criar promoção na Simplo7 se o usuário pedir |

`tablePrice` é o preço de venda normal (preço de tabela). `installmentPrice` costuma ser ~20% menor — é o preço à vista/promocional já calculado pela regra de precificação do Campaign Manager, não "preço parcelado" apesar do nome.

**Por que não confiar no Bling pra preço de venda:** o campo `preco` do Bling (via `nexus-manager.js`, skill `receitas-manager`) pode estar desatualizado ou ser custo mal cadastrado. Exemplo real: ao criar a linha "Bicama em Molas", o Bling mostrava o tamanho solteiro (menor) mais caro que a viúva (maior) — inconsistência que não existia no catálogo do Campaign Manager. Use Bling só se o modelo não existir no Campaign Manager.

`stock` já vem sincronizado do Bling (`stockSyncedAt`). Quando vier `null` (nunca sincronizado), tratar como incerto — assumir uma quantidade pequena (ex: 1) e avisar o usuário que é uma suposição.

## Passo 2 — Confirmar marca e categoria na Simplo7

```bash
curl -s -H "appKey: $SIMPLO7_APP_KEY" "https://senhorcolchao.com.br/ws/wsmarcas.json"
```

Marcas já conhecidas: MIRABOX=20, FA COLCHÕES=1, CASTOR=5, SENSOR=25, BECFLEX=41, PLUMATEX=55, BOX ROPAC MASTER BLIND=36 (marca errada que aparece em produtos antigos — corrigir pra marca real quando for o caso).

Categoria: existem **3 árvores raiz separadas**, não confundir:

| Raiz (parent null) | O que é | Sub "MOLAS"/tipo |
|---|---|---|
| `200` Colchões | Colchão avulso (sem base) | `206` MOLAS · `236` ESPUMA |
| `193` Cama Box + Colchão | Conjunto (colchão + base) | `181` MOLAS · `237` ESPUMA |
| `212` Cama Box | Base avulsa (sem colchão), inclui Box Baú e Bicama | `225` BOX BAÚ · `218` BOX COM AUXILIAR (bicama) |

Buscar a árvore completa quando precisar de um leaf novo:

```bash
curl -s -H "appKey: $SIMPLO7_APP_KEY" "https://senhorcolchao.com.br/ws/wscategorias.json"
```

## Passo 3 — Montar a combinação (variação) certa pro tipo de produto

**Isso é o erro mais comum: cada tipo de produto tem um conjunto de variações diferente.** Não presumir que o padrão de uma categoria vale pra outra.

| Tipo de produto | Variações (nessa ordem) | Grupos |
|---|---|---|
| **Colchão avulso** (sem base) | Altura do Colchão + Largura x Comprimento + Peso máximo suportado por pessoas | `46` + `48` + `49` |
| **Cama Box com colchão** (conjunto) | Largura x Comprimento + Nível de Conforto + Peso máximo suportado por pessoas | `48` + `40` + `49` |
| **Cama Box sem colchão** (base avulsa, Box Baú, Bicama) | Largura x Comprimento + Tamanho | `48` + `50` |

`Tamanho` (grupo 50) só entra na base avulsa (sem colchão) — nunca em colchão nem em conjunto cama-box-com-colchão. Isso já causou um cadastro errado uma vez (linha Prime): criei com Largura x Comprimento + Tamanho copiando o padrão de Box Suede, tive que apagar e recriar com o conjunto certo.

### Tabela de grupos e atributos (consultar antes de assumir um id de cabeça)

```bash
curl -s -H "appKey: $SIMPLO7_APP_KEY" "https://senhorcolchao.com.br/ws/wscombinacoes/<grupo>.json"
```

- **Grupo 40 — Conforto**: 166 Macio · 158 Intermediário · 156 Firme · 157 Extra Firme
- **Grupo 46 — Altura do Colchão**: 173=12cm 211=13cm 174=14cm 175=17cm 177=18cm 178=20cm 212=22cm 179=24cm 214=25cm 180=26cm 215=27cm 216=28cm 182=30cm 219=31cm 183=32cm 218=33cm 229=34cm 213=36cm
- **Grupo 48 — Largura x Comprimento**: 189=0,78x1,88m 190=0,88x1,88m 191=0,97x2,03m 192=1,28x1,88m 193=1,38x1,88m 194=1,58x1,98m 195=1,93x2,03m
- **Grupo 49 — Peso máximo suportado por pessoas**: 196=50kg 197=60kg 198=80kg 199=100kg 217=110kg 200=120kg 201=130kg 202=140kg 203=150kg — **atenção**: existe um segundo atributo "120 kg" com id `228`, duplicado; usei `200` (mais antigo, sequência original) mas vale reconfirmar se o painel reclamar.
- **Grupo 50 — Tamanho**: 204 Solteiro · 205 Viúva · 206 Casal · 207 Queen · 208 King

## Passo 4 — Criar o produto (POST)

```bash
curl -s -X POST \
  -H "appKey: $SIMPLO7_APP_KEY" -H "Content-Type: application/json" \
  "https://senhorcolchao.com.br/ws/wsprodutos.json" \
  -d '{
    "Wsproduto": {
      "tipo_cadastro": 1,
      "situacao": 1,
      "nome": "NOME EM MAIÚSCULO COMO O PADRÃO DA LOJA",
      "marca_id": 55,
      "descricao": "<html do template, ver pagina-produto-simplo7>",
      "disponivel": true,
      "vitrine": false,
      "frete_gratis": true,
      "sku": "20409151",
      "tag_h1": "...",
      "meta_title": "... | Senhor Colchão",
      "meta_keywords": "",
      "meta_description": "..."
    },
    "WsprodutoImagem": [
      { "principal": true, "ordem": 0, "imagem": "https://supabase.senhorcolchao.com/.../cena.jpg" },
      { "principal": false, "ordem": 1, "imagem": "https://supabase.senhorcolchao.com/.../plain.jpg" }
    ],
    "WsprodutoEstoque": [{
      "sku": "20409151",
      "quantidade": 1,
      "valor_compra": 743.98,
      "valor_venda": 929.90,
      "compra_minima": 1,
      "compra_maxima": 0,
      "altura": 25,
      "largura": 88,
      "comprimento": 188,
      "combinacao1_id": 46, "combinacao_atributo1_id": 214,
      "combinacao2_id": 48, "combinacao_atributo2_id": 190,
      "combinacao3_id": 49, "combinacao_atributo3_id": 200
    }],
    "WsprodutoCategoria": [{ "categoria_id": 207, "principal": true }]
  }'
```

Regras críticas:

- Enviar **só a categoria-folha** em `WsprodutoCategoria` — a API deriva pai/avô sozinha. Enviar a cadeia inteira manualmente duplica.
- `tipo_cadastro: 1` e os `combinacao*_id`/`combinacao_atributo*_id` **têm que estar presentes desde este POST inicial**. Retrofitar via `PUT /ws/wsprodutos/{id}.json` depois não funciona direito (o painel admin não reconhece a variação de verdade, mesmo a API aceitando e salvando).
- Se errar a combinação depois de já ter criado: `DELETE /ws/wsprodutos/{id}.json` funciona direto (não é bloqueado) e recriar do zero é mais seguro do que tentar corrigir por PUT.
- O campo de descrição do body é `descricao` (a doc oficial da Simplo7 mostra `decricao`, sem "s" — é typo da doc, o campo real é `descricao`).

## Passo 5 — Verificar

```bash
curl -s -H "appKey: $SIMPLO7_APP_KEY" "https://senhorcolchao.com.br/ws/wsprodutos/<id>.json"
```

Conferir: `sku`, `marca_id`, `tipo_cadastro`, categoria (folha + pai + avô auto-derivados), as 3 (ou 2) combinações certas pro tipo de produto, `valor_venda`, e a contagem de imagens na `descricao` — **conferir contra a skill certa do Passo 0**: produto único espera 2 fotos (Hero + Medidas, mesmo arquivo); conjunto cama box espera normalmente 5 fotos diferentes (Hero + Colchão + Base Box + 2 miniaturas de Medidas), só repetindo se faltar alguma versão "-cena" no bucket.

## Checklist final

1. Escolhi a skill certa pra montar o HTML (`pagina-produto-simplo7` pra produto único, `pagina-cama-box` pra conjunto) antes de escrever qualquer seção.
2. Busquei SKU/custo/preço no `/api/products/admin` do Campaign Manager, não no Bling.
3. Confirmei `marca_id` certo.
4. Escolhi a árvore de categoria certa (Colchões avulso / Cama Box+Colchão / Cama Box sem colchão) e a categoria-folha.
5. Montei a combinação certa pro tipo (colchão = altura+larg.compr+peso; cama box com colchão = larg.compr+conforto+peso; cama box sem colchão = larg.compr+tamanho).
6. Criei com `tipo_cadastro:1` e combinação já no POST inicial.
7. Verifiquei via GET antes de reportar como pronto, incluindo a contagem de fotos certa pro tipo de página (Passo 0).
