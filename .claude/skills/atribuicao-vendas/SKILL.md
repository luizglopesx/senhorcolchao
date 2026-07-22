---
name: atribuicao-vendas
description: >
  Cruza anúncios pagos (Meta Ads/Google Ads) com conversas reais no Campaign Manager e
  vendas confirmadas no Bling, pra saber quais anúncios geraram venda de verdade — não só
  clique ou conversa. Usa a mensagem automática do WhatsApp (autofill) como chave de
  atribuição, e o telefone do contato como chave entre Campaign Manager e Bling.
  Use quando o usuário perguntar "esse anúncio vendeu?", "qual campanha gerou venda",
  "cruza os leads com o Bling", "atribuição de vendas", ou /atribuicao-vendas.
---

# /atribuicao-vendas — Cruzamento de anúncio → conversa → venda real

Fecha o funil completo: anúncio pago → conversa no WhatsApp → pedido de venda no Bling.
Sem isso, só sabemos quantas "conversas iniciadas" um anúncio gerou (métrica do Meta) — não
se isso virou dinheiro de verdade.

## Pré-requisito obrigatório

**Cada anúncio precisa ter uma mensagem automática (autofill) distinta e específica no
CTA de WhatsApp**, configurada no criativo (`page_welcome_message`, campo `autofill_message`).
Sem isso, não tem como saber de qual anúncio uma conversa veio.

Padrão usado nesta conta (confirmado funcionando em 20/07/2026, campanha Pré-Festa do
Peão): mensagem no formato natural "Olá! Quero saber do [produto] de R$[preço] em 12x
sem juros." — melhor que um código artificial tipo "VEIO_DO_ANUNCIO_X", porque soa normal
pro cliente E ainda serve como identificador único pra busca.

Isso é montado via `create_video_creative` do `meta_ads_client.py`
(`.claude/skills/social-post-scheduler/scripts/`), parâmetro `autofill_message`. Se o
anúncio já existe sem essa mensagem, é preciso criar um criativo novo com a mensagem e
apontar o anúncio pra ele (criativo do Meta é imutável, não dá pra editar o existente).

## Workflow

### Passo 1 — Buscar leads no Campaign Manager

Pra cada anúncio, buscar pela **frase exata da mensagem automática** (não só o nome do
produto — ver Regras abaixo) em **ambas as views**, `active` e `archived` (compradores
confirmados costumam ser arquivados com a label "Comprou").

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
for VIEW in active archived; do
  curl -s -G -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
    --data-urlencode "view=$VIEW" \
    --data-urlencode "search=Quero saber do [produto] de R\$[preço]" \
    "$BASE_URL/api/conversations"
done
```

Guardar de cada resultado: `customerName`, `customerPhone`, `lastActivity`, `labels`.

**Filtrar por data:** descartar resultados com `lastActivity` anterior ao lançamento da
campanha — busca por texto pode achar conversas antigas não relacionadas (ver Regras).

**Importante — a busca só olha a última mensagem (`preview`), não o histórico todo.**
Assim que o atendente responde e o lead é classificado (ex: label "Meio"), a conversa sai
da busca por texto — o `preview` vira a resposta do atendente/cliente, não mais a mensagem
automática de origem. Isso NÃO significa que o lead sumiu: ele normalmente é movido pro
motor de follow-up. Sempre checar também:

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
curl -s -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  "$BASE_URL/api/follow-up/executions"
```

Cada execução traz `conversation.customerName`, `conversation.customerPhone` e
`conversation.labels` — cruzar por `conversationId` com o que já foi achado na busca de
texto pra não contar duas vezes, e usar isso pra recuperar leads que "sumiram" da busca
principal.

### Passo 2 — Listar pedidos de venda no Bling no período da campanha

```bash
BASE_URL="${RECEITAS_MANAGER_URL%/}"
curl -s -H "Authorization: Bearer $RECEITAS_MANAGER_TOKEN" \
  "$BASE_URL/api/nexus-manager?resource=bling-pedidos-vendas&dataInicial=YYYY-MM-DD&dataFinal=YYYY-MM-DD&limit=100"
```

Retorna `numero`, `data`, `total`, `contato.id`, `contato.nome`. **Não traz telefone.**

### Passo 3 — Buscar telefone de cada contato do pedido

```bash
BASE_URL="${RECEITAS_MANAGER_URL%/}"
curl -s -H "Authorization: Bearer $RECEITAS_MANAGER_TOKEN" \
  "$BASE_URL/api/nexus-manager?resource=bling-contato&id=<contato.id>"
```

Retorna `telefone` e `celular`, formato `(17) 99237-9459`.

### Passo 4 — Normalizar e cruzar telefones

Campaign Manager usa formato `55` + DDD + número (ex: `5517992379459`). Bling usa
`(17) 99237-9459`. Normalizar os dois pra só dígitos antes de comparar (remover `55` do
prefixo do Campaign Manager, remover tudo que não for dígito do Bling).

### Passo 5 — Montar a tabela final

| Anúncio | Leads (conversas) | Vendas confirmadas | Faturamento |
|---|---|---|---|
| Nome do anúncio | N | N | R$ X |

## Regras

- **Nunca buscar só pelo nome do produto** (ex: "D28 Comfortopedic") — pega falso positivo
  de conversas antigas não relacionadas à campanha atual, que mencionaram o produto por
  outro motivo. Sempre usar a frase completa da mensagem automática.
- **Sempre checar `archived` além de `active`** — cliente que já comprou costuma ser
  arquivado com label "Comprou" nesta conta, então ficaria invisível numa busca só em
  `active`.
- **Telefone é a chave confiável, nome não é** — nome digitado pode variar (apelido,
  nome de outra pessoa da família fazendo o pedido, "CONSUMIDOR FINAL" genérico). Sempre
  cruzar por telefone quando disponível.
- **Não inventar venda.** Se não achar telefone batendo, o resultado é "0 vendas
  confirmadas" — não estimar ou arredondar pra cima.
- **Timing:** produto de ticket alto (colchão, cama box) não converte no mesmo dia
  normalmente — não estranhar 0 venda nos primeiros 1-3 dias de campanha.
- Fonte do endpoint `bling-contato`: adicionado em `Projeto Receitas 2/api/nexus-manager.js`
  em 21/07/2026, seguindo o mesmo padrão dos outros resources `bling-*`. GET-only.
