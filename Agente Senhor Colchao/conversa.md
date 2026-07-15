# Agente Senhor Colchão — Consulta via WhatsApp (Bling)

Registro da conversa de planejamento (2026-07-15) pra continuar depois.

## Ideia original

Ter um agente de IA acessível pelo WhatsApp: manda uma pergunta sobre estoque
(depois expandido pra vendas e custo) no Bling, e recebe a resposta automaticamente,
sem precisar abrir o Claude Code.

## O que já existe hoje (levantado durante a conversa)

- **Bling ERP** — acesso somente leitura já funciona via `nexus-manager.js`
  (projeto `Projeto Receitas 2/api/nexus-manager.js`), exposto pelo Receitas Manager
  (`RECEITAS_MANAGER_URL` / `RECEITAS_MANAGER_TOKEN`, já no `.env` do MazyOS).
  - Resources já implementados: `bling-produtos`, `bling-produto`, `bling-estoque`,
    `bling-pedidos-vendas`, `bling-pedido-venda`, `bling-nfe`, `bling-nfe-detalhe`.
  - Token do Bling é gerenciado numa planilha Google (célula B2), renovado a cada ~4h
    (`fetchBlingToken` em `nexus-manager.js`).
  - Integração é **GET-only por construção** (sem risco de escrita acidental no Bling).

- **Campaign Manager** (`Projetos/Campaign Manager`) — backend real (Node/TS + Prisma),
  deploy automático via GitHub Actions pra Swarm (`campaign_backend` / `campaign_frontend`).
  - Cada número de WhatsApp conectado é um `ConversationChannel` no banco.
  - Mensagens inbound chegam via WuzAPI → webhook (`routes/webhook.ts`) → cria/atualiza
    conversa → dispara `runInboundAutomationRules` com trigger `INBOUND_MESSAGE`
    (`services/automation-rules.ts`).
  - Ações hoje disponíveis nesse motor de automação são fixas: `SEND_QUICK_REPLY`,
    `APPLY_LABEL`, `START_FOLLOW_UP`, `ASSIGN_USER`, `START_CAMPAIGN`, `MOVE_TO_STAGE` etc.
    **Nenhuma delas consulta API externa dinamicamente nem gera resposta livre com IA.**
  - Já existe padrão de chamada de IA no backend: `follow-up-ai-message-service.ts`,
    hoje usando OpenAI `gpt-4o-mini`, configurável em `Settings.aiProvider`.
  - Envio de mensagem de volta pro WhatsApp já existe: `POST /api/conversations/:id/send`.
  - **Importante:** o model `AutomationRule` no Prisma **não tem campo de canal/telefone** —
    uma regra vale pra qualquer número conectado. Filtro por remetente precisaria ser
    escrito no código da ação nova, não é uma opção de tela hoje.

## Descoberta sobre custo de produto no Bling

- `/produtos` (já usado) só traz `preco` (preço de venda), **não** tem custo.
- Preço de custo (`precoCusto`, `precoCompra`) mora em `/produtos/fornecedores`
  (vínculo produto-fornecedor), endpoint **ainda não exposto** no `nexus-manager.js`.
  Precisaria virar um resource novo (`bling-produto-fornecedor`), seguindo o mesmo
  padrão dos 7 que já existem (~15 linhas de código).

## Vendas diárias / por período

- `bling-pedidos-vendas` já aceita `dataInicial`/`dataFinal` (e `idVendedor`, `idLoja`).
  Já dá pra buscar vendas de um dia ou período — só falta uma camada de agregação
  (somar `valorTotal` por dia/vendedor/produto). Não precisa de chamada nova ao Bling.

## Catálogo completo do Bling (referência)

Existe um Postman collection salvo em
`Projeto Receitas 2/api/bling-api.postman_collection.json` com todos os endpoints
disponíveis (contas a pagar/receber, categorias, vendedores, contratos, NFe/NFCe/NFSe etc).
Vale checar antes de expor `contas/receber`/`contas/pagar` do Bling se isso não duplica
o que o Receitas Manager já trata como fonte de verdade.

## Segunda hipótese (a que ficou decidida)

Existe hoje um número de WhatsApp **já cadastrado numa API**, usado só pra consulta de
estoque via **n8n** — mas é lento (workflow pagina de 20 em 20 com espera entre páginas,
ver `Projetos/Automacao Estoque/Workflow Relatorio Estoque Supabase.json`) e limitado só
a estoque.

Ideia: migrar esse número pro Campaign Manager (vira um `ConversationChannel` novo lá) e
liberar acesso ao agente de IA pra dois números: o do usuário e o do pai (os dois que
administram a loja).

**Ponto técnico confirmado na conversa:** WuzAPI (e providers não-oficiais equivalentes)
permite só um consumidor de webhook por sessão/número. "Cadastrar no CM" na prática é
**migrar** — tirar do n8n e conectar como canal novo no CM — não rodar os dois em paralelo
na mesma linha. Isso foi confirmado como intenção: aposentar o fluxo n8n de estoque assim
que o agente novo estiver de pé.

## Decisões tomadas

1. **Escopo de resposta automática:** só responde quando o remetente é um número autorizado
   (não é um bot aberto pra qualquer cliente). Confirmado.
2. **Números autorizados:** o do usuário (Luiz Gustavo) + o do pai — os dois administradores
   da loja.
3. **Nível de acesso do pai:** **igual ao do usuário** — acesso completo (estoque, vendas e
   custo/margem), sem restrição.
4. **Dados a disponibilizar:** estoque, vendas (diária/por período) e custo de produto —
   não só estoque como é hoje no n8n.

## Desenho final do fluxo

1. WhatsApp → WuzAPI → webhook do Campaign Manager (`routes/webhook.ts`).
2. Cria/atualiza a conversa, dispara automação com trigger `INBOUND_MESSAGE`.
3. Ação nova (a construir) checa se o remetente está na lista dos 2 números autorizados.
   - Se não estiver: segue fluxo normal (esse canal hoje não atende cliente, mas a trava
     fica no código por segurança/clareza).
4. Se estiver: consulta o Bling via Receitas Manager (`bling-produtos`, `bling-estoque`,
   `bling-pedidos-vendas`, e o novo `bling-produto-fornecedor` pra custo).
5. Gera resposta em linguagem natural com IA (reaproveitando o padrão já usado em
   `follow-up-ai-message-service.ts`).
6. Envia de volta na mesma conversa via `POST /api/conversations/:id/send` (endpoint
   já existente).

## Próximos passos (em aberto)

- [ ] Decidir: escrever um plano formal de implementação (arquivos exatos, ordem dos
      passos, o que testar antes de desligar o n8n) antes de mexer no código, ou já
      começar a implementar direto.
- [ ] Migrar o número do n8n pro Campaign Manager (conectar como `ConversationChannel` novo).
- [ ] Implementar o resource `bling-produto-fornecedor` no `nexus-manager.js`.
- [ ] Implementar a agregação de vendas (diária/período) a partir de `bling-pedidos-vendas`.
- [ ] Implementar a ação nova de automação no Campaign Manager (filtro de telefone +
      busca no Bling + geração de resposta + envio).
- [ ] Testar de ponta a ponta antes de desligar o fluxo n8n atual.

## Onde as coisas vivem (referência rápida)

- `Projetos/Senhor Colchao/senhor-colchao/` — MazyOS, memória e skills da operação
  (marketing, financeiro, etc.), onde essa conversa começou.
- `Projetos/Projeto Receitas 2/api/nexus-manager.js` — proxy do Receitas Manager +
  acesso somente-leitura ao Bling.
- `Projetos/Campaign Manager/` — backend/frontend do WhatsApp (Node/TS, Prisma, deploy
  via GitHub Actions).
- `Projetos/Automacao Estoque/` — workflow n8n atual de estoque (o que será aposentado).
