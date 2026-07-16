# Briefing pro Claude Code do projeto Campaign Manager

Cole esse arquivo (ou peça pro Claude ler ele) numa sessão aberta direto no projeto
`Campaign Manager`. Ele resume tudo que foi decidido numa conversa de planejamento
feita no projeto `Senhor Colchao/senhor-colchao` (pasta `Agente Senhor Colchao/`,
arquivo `conversa.md` — histórico completo lá se precisar de mais contexto).

## O que construir

Um agente de IA que responde perguntas sobre **estoque, vendas e custo de produto**
(dados do Bling ERP) direto pelo WhatsApp, pra duas pessoas específicas que administram
a loja (Luiz Gustavo e o pai dele). Hoje isso é feito de forma limitada e lenta via n8n
(só estoque, workflow paginado e lento) — a ideia é substituir esse fluxo por algo
embutido no próprio Campaign Manager.

## Decisões já fechadas (não reabrir sem necessidade)

1. **Quem recebe resposta automática:** só os números autorizados (Luiz Gustavo + pai).
   Qualquer outro remetente segue o atendimento normal, sem IA no meio.
2. **Nível de acesso:** igual pros dois números — estoque, vendas e custo/margem,
   sem restrição entre eles.
3. **Dados disponíveis:** estoque atual, vendas por dia/período, custo de produto —
   não só estoque.
4. **Onde mora a integração com o Bling:** **direto neste projeto** (Campaign Manager),
   não via proxy do Receitas Manager (`nexus-manager.js`, projeto `Projeto Receitas 2`).
   Motivo: `nexus-manager.js` roda como função serverless na Vercel e sofre cold start
   (200ms a mais de 1s na primeira chamada depois de um tempo parado). O Campaign
   Manager é um serviço sempre rodando (Docker/Swarm) — sem esse problema, e o cache do
   token do Bling em memória sobrevive de verdade entre chamadas.
5. **Escopo da integração com o Bling:** só os endpoints que esse agente usa. Não
   precisa portar tudo do `nexus-manager.js`, só a fatia relevante (ver abaixo).
   **GET-only** — sem nenhum caminho de escrita no Bling, por segurança.
6. **Número de WhatsApp:** vai ser migrado do n8n pra cá (vira um `ConversationChannel`
   novo). Isso desliga o webhook do n8n nesse número — não dá pra rodar os dois ao
   mesmo tempo na mesma linha (o provedor de WhatsApp só aceita um consumidor de
   webhook por sessão).

## Arquitetura de referência (o que já existe no Campaign Manager)

- Mensagem inbound chega via WuzAPI → webhook (`src/routes/webhook.ts`) → cria/atualiza
  conversa → dispara `runInboundAutomationRules` (`src/services/automation-rules.ts`)
  com trigger `INBOUND_MESSAGE`.
- O model `AutomationRule` (`prisma/schema.prisma`) **não tem campo de canal/telefone**
  — uma regra vale pra qualquer número conectado. O filtro pelos 2 números autorizados
  precisa ser escrito no código da ação nova, não dá pra configurar isso numa tela hoje.
- Ações hoje suportadas em `automation-rules.ts` são fixas (`SEND_QUICK_REPLY`,
  `APPLY_LABEL`, `START_FOLLOW_UP`, `ASSIGN_USER`, `START_CAMPAIGN`, `MOVE_TO_STAGE`
  etc.) — nenhuma consulta API externa dinamicamente. Precisa de uma ação nova.
- Já existe um padrão de chamada de IA no backend: `src/services/follow-up-ai-message-service.ts`
  (hoje usa OpenAI `gpt-4o-mini`, configurável em `Settings.aiProvider`). Reaproveitar
  esse padrão pra gerar a resposta em linguagem natural.
- Envio de mensagem de volta pro WhatsApp já existe e não precisa de nada novo:
  `POST /api/conversations/:id/send` (`src/routes/conversations.ts`).

## Cliente Bling a construir (baseado no `nexus-manager.js` do Receitas Manager)

Reimplementar como serviço próprio (ex: `src/services/bling-client.ts`), copiando a
lógica de `Projeto Receitas 2/api/nexus-manager.js` (linhas ~244–441 daquele arquivo),
adaptada pro estilo do Campaign Manager:

- **Token do Bling:** vem de uma célula (B2) numa planilha Google, renovado a cada
  ~10min de cache local (o token em si dura ~4h no Bling). Precisa de Service Account
  do Google (`GOOGLE_SERVICE_ACCOUNT_JSON`) e `GOOGLE_SHEETS_SPREADSHEET_ID` — pedir
  essas credenciais pro Luiz Gustavo (são as mesmas já usadas no Receitas Manager).
- **Throttle:** mínimo 700ms entre chamadas ao Bling (evita 429).
- **Retry:** em 401 ou resposta HTML, renova o token e tenta de novo; em 429, retry
  com backoff (até 3 tentativas).
- **Base URL Bling:** `https://api.bling.com.br/Api/v3`.

Endpoints a cobrir (todos GET, todos com paginação/filtros do Bling v3):

| Uso | Endpoint Bling | Observação |
|---|---|---|
| Buscar produto por nome/código | `GET /produtos?nome=...&codigo=...` | Retorna lista |
| Detalhe do produto | `GET /produtos/{id}` | Traz `preco` (venda), **não** custo |
| Saldo de estoque | `GET /estoques/saldos?idsProdutos[]=...` | Precisa dos IDs dos produtos primeiro |
| Vendas por período | `GET /pedidos/vendas?dataInicial=...&dataFinal=...` | Pra "vendas diárias" usar dataInicial=dataFinal=hoje; agregar (somar `valorTotal`) no código, o Bling não devolve totalizado |
| Custo de produto | `GET /produtos/fornecedores?idProduto=...` | Campo `precoCusto` / `precoCompra` — **custo não está em `/produtos`**, é endpoint separado |

Há um Postman collection completo do Bling salvo em
`Projeto Receitas 2/api/bling-api.postman_collection.json`, com todos os endpoints e
exemplos de resposta, caso precise de mais campos.

## Ação nova de automação

Sugestão de nome: `AI_STOCK_LOOKUP` (ou nome que fizer mais sentido no enum
`AutomationRuleAction` do Prisma).

Fluxo dentro da ação, disparada pelo trigger `INBOUND_MESSAGE`:

1. Pega o telefone do remetente da mensagem (via `conversation`/`contact` ligado ao
   `messageId` do contexto de execução).
2. Compara contra uma whitelist de 2 números (Luiz Gustavo + pai) — hardcoded no
   código ou em variável de ambiente, não em config de tela (ver limitação do model
   `AutomationRule` acima).
3. Se não bater: não faz nada (deixa o fluxo normal seguir).
4. Se bater: interpreta a pergunta (texto da mensagem), decide que dado buscar no
   Bling (produto/estoque/vendas/custo), chama o `bling-client.ts` novo.
5. Gera a resposta em linguagem natural com IA, reaproveitando o padrão de
   `follow-up-ai-message-service.ts` (mesmo provedor/config de IA já configurado em
   `Settings`).
6. Envia a resposta de volta com `POST /api/conversations/:id/send`.

## Passos sugeridos de implementação

1. `src/services/bling-client.ts` — cliente Bling novo (token, throttle, os 5 endpoints
   da tabela acima), GET-only.
2. Variáveis de ambiente novas: `GOOGLE_SERVICE_ACCOUNT_JSON`, `GOOGLE_SHEETS_SPREADSHEET_ID`
   (adicionar em `.env.example` e no ambiente de produção via secrets do deploy).
3. Nova action `AI_STOCK_LOOKUP` em `automation-rules.ts` + no enum do Prisma
   (`AutomationRuleAction`) + migration.
4. Whitelist de telefones autorizados (definir onde: env var tipo
   `STOCK_AGENT_AUTHORIZED_PHONES=5517999999999,5517988888888` é o mais simples).
5. Função de agregação de vendas (somar por dia/período a partir de `pedidos/vendas`).
6. Testar a ação isolada (sem depender do WhatsApp real) antes de ligar no canal.
7. Conectar o número (hoje no n8n) como `ConversationChannel` novo no Campaign Manager.
8. Criar a `AutomationRule` habilitada com trigger `INBOUND_MESSAGE` e action
   `AI_STOCK_LOOKUP` nesse canal.
9. Testar de ponta a ponta mandando pergunta real pelo WhatsApp.
10. Só depois de validado, desligar o webhook do n8n pra esse número.

## O que NÃO fazer

- Não dar nenhum caminho de escrita no Bling (só GET).
- Não responder pra números fora da whitelist.
- Não reaproveitar o `nexus-manager.js` do Receitas Manager pra esse fluxo (é essa a
  decisão de arquitetura — Bling mora aqui agora, direto).
