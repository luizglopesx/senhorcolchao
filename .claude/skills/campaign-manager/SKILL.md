---
name: campaign-manager
description: "Acesso direto ao Campaign Manager via API. Use quando o usuário perguntar sobre contatos, conversas, mensagens, campanhas de WhatsApp, métricas, labels, dashboard ou follow-up."
---

# Campaign Manager Integration

Use esta skill para consultar e operar o Campaign Manager da Senhor Colchão.

Base URL: `https://messenger.senhorcolchao.com`

Token: variável `CAMPAIGN_MANAGER_TOKEN` do `.env`

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
```

Sempre enviar:
```
Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN
Content-Type: application/json
```

Nunca exibir tokens. Nunca expor o conteúdo do `.env`. Resumir respostas grandes em vez de colar JSON bruto.

## Health Check

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
curl -s \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  -H "Content-Type: application/json" \
  "$BASE_URL/api/health"
```

Se retornar 401: verificar que `CAMPAIGN_MANAGER_TOKEN` no `.env` está correto.
Se retornar 404: verificar que `CAMPAIGN_MANAGER_URL` é apenas a origin (sem trailing path).

## Leituras

### Dashboard
```bash
curl -s -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" "$BASE_URL/api/dashboard"
```

### Métricas
```bash
curl -s -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" "$BASE_URL/api/metrics"
```

### Contatos (paginado)
```bash
curl -s -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  "$BASE_URL/api/contacts?search=&page=1&limit=50&channelId="
```

### Lista compacta de contatos
```bash
curl -s -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" "$BASE_URL/api/contacts/all"
```

### Detalhes de um contato
```bash
curl -s -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  "$BASE_URL/api/contacts/<CONTACT_ID>/details"
```

### Conversas
```bash
curl -s -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  "$BASE_URL/api/conversations?view=active&search=&channelId="
```
`view` pode ser `active` ou `archived`.

### Mensagens de uma conversa
```bash
curl -s -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  "$BASE_URL/api/conversations/<CONVERSATION_ID>/messages"
```

### Campanhas
```bash
curl -s -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  "$BASE_URL/api/campaigns?status=&page=1&limit=50"
```

### Follow-Up Playbooks
```bash
curl -s -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" "$BASE_URL/api/follow-up/playbooks"
```

### Follow-Up Execuções
```bash
curl -s -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" "$BASE_URL/api/follow-up/executions"
```

## Escritas

Pedir confirmação explícita antes de qualquer escrita. A confirmação deve nomear a operação, o alvo e o efeito esperado.

### Atualizar labels de uma conversa
```bash
curl -s -X PUT \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"labels":["label-a","label-b"]}' \
  "$BASE_URL/api/conversations/<CONVERSATION_ID>/labels"
```

### Adicionar nota a uma conversa
```bash
curl -s -X POST \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content":"Texto da nota."}' \
  "$BASE_URL/api/conversations/<CONVERSATION_ID>/notes"
```

### Iniciar conversa
```bash
curl -s -X POST \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channelId":"<channel-id>","phone":"5517999999999","name":"Nome do contato"}' \
  "$BASE_URL/api/conversations/start"
```

### Criar campanha
```bash
curl -s -X POST \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Nome da campanha","description":"Descrição"}' \
  "$BASE_URL/api/campaigns"
```

### Adicionar destinatários a uma campanha
```bash
curl -s -X POST \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"recipients":[{"phone":"5517999999999","name":"Nome"}]}' \
  "$BASE_URL/api/campaigns/<CAMPAIGN_ID>/recipients"
```

### Iniciar campanha
```bash
curl -s -X POST \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  "$BASE_URL/api/campaigns/<CAMPAIGN_ID>/start"
```

### Ação em follow-up
Ações suportadas: `resume`, `reactivate`, `restart`, `cancel`
```bash
curl -s -X POST \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  "$BASE_URL/api/follow-up/executions/<EXECUTION_ID>/<ACTION>"
```

## Tratamento de respostas

- Para listas grandes: resumir contagens, totais, nomes, datas e status
- Para conversas: não colar histórico completo a menos que solicitado
- Para campanhas: destacar status, ações pendentes e próximos passos
