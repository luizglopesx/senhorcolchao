---
name: custom-int-campaign-manager
description: "Direct Campaign Manager API access. Use when the user asks about Campaign Manager, CM contacts, conversations, messages, campaigns, metrics, labels, dashboard, or follow-up executions."
---

# Campaign Manager Integration

Use this skill to consult and operate the Campaign Manager API.

Base URL:

```text
CAMPAIGN_MANAGER_URL
```

Bearer token:

```text
CAMPAIGN_MANAGER_TOKEN
```

Always normalize the base URL before making requests:

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
```

Always send:

```text
Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN
Content-Type: application/json
```

Never print tokens. Never expose `.env` contents. Summarize large API responses instead of pasting raw JSON.

## Required Environment Variables

In the EvoNexus workspace `.env`:

```env
CAMPAIGN_MANAGER_URL=https://messenger.senhorcolchao.com
CAMPAIGN_MANAGER_TOKEN=o-mesmo-valor-de-CAMPAIGN_MANAGER_API_TOKEN
```

`CAMPAIGN_MANAGER_TOKEN` is not a login JWT. It is a stable integration token validated by the Campaign Manager backend.

Do not put `CAMPAIGN_MANAGER_API_TOKEN` in Nexus documentation or responses. That variable belongs to the Campaign Manager backend/server environment.

## Health Check

Use this first when validating the integration:

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
curl -s \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  -H "Content-Type: application/json" \
  "$BASE_URL/api/health"
```

If this returns 401, check that `CAMPAIGN_MANAGER_TOKEN` in EvoNexus is exactly the same value as `CAMPAIGN_MANAGER_API_TOKEN` in the Campaign Manager backend.

If this returns 404, check that `CAMPAIGN_MANAGER_URL` is only the origin, for example:

```text
https://messenger.senhorcolchao.com
```

Do not use `/login`, `/api`, or a trailing path in `CAMPAIGN_MANAGER_URL`.

## Read Operations

Use read operations freely when the user asks for status, summaries, analysis, lists, or details.

### Dashboard

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
curl -s \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  "$BASE_URL/api/dashboard"
```

Purpose: overall dashboard summary.

### Metrics

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
curl -s \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  "$BASE_URL/api/metrics"
```

Purpose: campaign and follow-up metrics.

### Paginated Contacts

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
curl -s \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  "$BASE_URL/api/contacts?search=&page=1&limit=50&channelId="
```

Purpose: search and page through contacts.

### Compact Contact List

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
curl -s \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  "$BASE_URL/api/contacts/all"
```

Purpose: compact contact list for campaigns/broadcasts.

### Contact Details

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
CONTACT_ID="replace-with-contact-id"
curl -s \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  "$BASE_URL/api/contacts/$CONTACT_ID/details"
```

Purpose: full contact details and timeline.

### Conversations

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
curl -s \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  "$BASE_URL/api/conversations?view=active&search=&channelId="
```

Purpose: list conversations. `view` can be `active` or `archived`.

### Conversation Messages

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
CONVERSATION_ID="replace-with-conversation-id"
curl -s \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  "$BASE_URL/api/conversations/$CONVERSATION_ID/messages"
```

Purpose: conversation history.

### Campaigns

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
curl -s \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  "$BASE_URL/api/campaigns?status=&page=1&limit=50"
```

Purpose: list campaigns.

### Follow-Up Playbooks

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
curl -s \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  "$BASE_URL/api/follow-up/playbooks"
```

Purpose: list follow-up playbooks.

### Follow-Up Executions

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
curl -s \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  "$BASE_URL/api/follow-up/executions"
```

Purpose: list follow-up executions.

## Write Operations

Ask for explicit user confirmation before any write operation.

The confirmation must name the exact operation, target, and likely effect. Example:

```text
Vou adicionar a label X na conversa Y. Confirma?
```

Only proceed after the user confirms.

### Update Conversation Labels

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
CONVERSATION_ID="replace-with-conversation-id"
curl -s -X PUT \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"labels":["label-a","label-b"]}' \
  "$BASE_URL/api/conversations/$CONVERSATION_ID/labels"
```

### Add Conversation Note

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
CONVERSATION_ID="replace-with-conversation-id"
curl -s -X POST \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content":"Nota criada pelo EvoNexus."}' \
  "$BASE_URL/api/conversations/$CONVERSATION_ID/notes"
```

### Start Conversation

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
curl -s -X POST \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channelId":"replace-with-channel-id","phone":"5517999999999","name":"Nome do contato"}' \
  "$BASE_URL/api/conversations/start"
```

### Create Campaign

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
curl -s -X POST \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Nova campanha","description":"Criada pelo EvoNexus"}' \
  "$BASE_URL/api/campaigns"
```

### Update Campaign

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
CAMPAIGN_ID="replace-with-campaign-id"
curl -s -X PUT \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Nome atualizado"}' \
  "$BASE_URL/api/campaigns/$CAMPAIGN_ID"
```

### Add Campaign Recipients

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
CAMPAIGN_ID="replace-with-campaign-id"
curl -s -X POST \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"recipients":[{"phone":"5517999999999","name":"Nome"}]}' \
  "$BASE_URL/api/campaigns/$CAMPAIGN_ID/recipients"
```

### Start Campaign

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
CAMPAIGN_ID="replace-with-campaign-id"
curl -s -X POST \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  "$BASE_URL/api/campaigns/$CAMPAIGN_ID/start"
```

### Follow-Up Execution Actions

Supported actions:

```text
resume
reactivate
restart
cancel
```

Example:

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
EXECUTION_ID="replace-with-execution-id"
ACTION="resume"
curl -s -X POST \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  "$BASE_URL/api/follow-up/executions/$EXECUTION_ID/$ACTION"
```

### WhatsApp Status (Stories)

Base URL: `{CAMPAIGN_MANAGER_URL}/api/status`

#### Upload de mídia

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
curl -s -X POST \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  -F "media=@/path/to/file.mp4" \
  "$BASE_URL/api/status/upload"
```

Aceita: JPEG, PNG, WebP, GIF, MP4, WebM, MOV, AVI (máx 50MB).
Vídeos são processados automaticamente: cortados em 30s, convertidos para MP4/H.264, máx 720p.

Resposta: `{ "url": "https://supabase.../signed-url", "path": "...", "mediaType": "video", "videoDuration": 28 }`

#### Publicar imediatamente

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
curl -s -X POST \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"mediaUrl":"https://...","caption":"Texto opcional","mediaType":"video"}' \
  "$BASE_URL/api/status/publish"
```

#### Agendar publicação

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
curl -s -X POST \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"mediaUrl":"https://...","caption":"Texto opcional","mediaType":"video","scheduledFor":"2026-07-07T14:00:00.000Z"}' \
  "$BASE_URL/api/status/schedules"
```

`scheduledFor` deve ser em UTC (BRT = UTC-3, portanto 11h BRT = 14h UTC).

#### Listar agendamentos

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
curl -s \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  "$BASE_URL/api/status/schedules?status=PENDING&page=1&limit=20"
```

Status possíveis: `PENDING`, `SENT`, `FAILED`, `CANCELLED`

#### Editar agendamento pendente

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
SCHEDULE_ID="replace-with-id"
curl -s -X PUT \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"mediaUrl":"https://...","mediaType":"video","scheduledFor":"2026-07-07T14:00:00.000Z"}' \
  "$BASE_URL/api/status/schedules/$SCHEDULE_ID"
```

#### Cancelar agendamento

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
SCHEDULE_ID="replace-with-id"
curl -s -X DELETE \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  "$BASE_URL/api/status/schedules/$SCHEDULE_ID"
```

#### Histórico de publicações

```bash
BASE_URL="${CAMPAIGN_MANAGER_URL%/}"
curl -s \
  -H "Authorization: Bearer $CAMPAIGN_MANAGER_TOKEN" \
  "$BASE_URL/api/status/history"
```

**Fluxo completo para agendar:**
1. `POST /api/status/upload` → recebe a `url` da mídia
2. `POST /api/status/schedules` com a `url` + `scheduledFor` em UTC

## Response Handling

- For large lists, summarize counts, totals, names, dates, statuses, and the top items.
- For conversations, do not paste huge message histories unless the user asks.
- For campaigns/follow-up, highlight status, pending actions, failures, and next scheduled steps.
- Never expose raw tokens, auth headers, `.env`, or private credentials.
