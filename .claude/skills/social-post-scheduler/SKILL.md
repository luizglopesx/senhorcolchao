---
name: social-post-scheduler
description: "Agenda posts no Instagram e Facebook automaticamente via Meta Graph API. Use quando o usuário quiser agendar um post, programar publicação, agendar para uma data específica, ou quando mencionar 'agendar post', 'programar publicação', 'postar no dia X'. Suporta foto, carrossel e posts no Facebook."
---

# Social Post Scheduler

Agenda publicações no Instagram e Facebook via Meta Graph API — sem precisar abrir o Meta Business Suite.

## Conta disponível

- `senhor_colchao` — Instagram @senhorcolchao + Página Senhor Colchão

## Como usar esta skill

Quando o usuário quiser agendar um post:

1. **Colete as informações** necessárias (veja Input Gathering abaixo)
2. **Converta a data/hora** para Unix timestamp (fuso: America/Sao_Paulo = UTC-3)
3. **Execute o scheduler** via script Python
4. **Confirme** com os IDs retornados

## Input Gathering

Pergunte apenas o que o usuário não forneceu:

- **Arte**: caminho do arquivo PNG/JPG ou URL pública da imagem
- **Legenda**: texto do post (se não fornecida, peça ou gere)
- **Data e hora**: ex: "19/05 às 10h" → converta para Unix timestamp
- **Plataforma(s)**: Instagram, Facebook ou ambos (padrão: ambos)
- **Tipo**: feed, carrossel ou story (padrão: feed)

Se o usuário fornecer tudo, execute direto sem perguntar.

## Conversão de data para Unix timestamp

Fuso horário: America/Sao_Paulo (UTC-3)
Fórmula: timestamp_utc = timestamp_local + 3*3600

Exemplos:
- "19/05/2026 às 10h" → 2026-05-19 10:00 BRT → 2026-05-19 13:00 UTC → unix: 1747656000
- "26/05/2026 às 09h" → unix: 1748257200

## Execução

```bash
# Agendar foto no Instagram
python3 {project-root}/.claude/skills/social-post-scheduler/scripts/instagram_publisher.py schedule_photo <image_url> "<caption>" <unix_ts>

# Agendar foto no Facebook
python3 {project-root}/.claude/skills/social-post-scheduler/scripts/facebook_publisher.py schedule_post "<message>" <unix_ts> [image_url]

# Agendar carrossel no Instagram
python3 {project-root}/.claude/skills/social-post-scheduler/scripts/instagram_publisher.py schedule_carousel <img1,img2,img3> "<caption>" <unix_ts>

# Publicar imediatamente no Instagram
python3 {project-root}/.claude/skills/social-post-scheduler/scripts/instagram_publisher.py publish_photo <image_url> "<caption>"

# Publicar imediatamente no Facebook
python3 {project-root}/.claude/skills/social-post-scheduler/scripts/facebook_publisher.py publish_post "<message>" [image_url]

# Listar posts agendados
python3 {project-root}/.claude/skills/social-post-scheduler/scripts/instagram_publisher.py scheduled
python3 {project-root}/.claude/skills/social-post-scheduler/scripts/facebook_publisher.py scheduled

# Ver contas configuradas
python3 {project-root}/.claude/skills/social-post-scheduler/scripts/instagram_publisher.py accounts
python3 {project-root}/.claude/skills/social-post-scheduler/scripts/facebook_publisher.py accounts
```

## Importante: imagens precisam de URL pública

A Meta Graph API exige URLs públicas para as imagens (não aceita caminhos locais).

Se o usuário fornecer um arquivo local (ex: `marketing/arte.png`), use o script de upload:

```bash
python3 {project-root}/.claude/skills/social-post-scheduler/scripts/upload_image.py <caminho_local>
```

Ele retorna uma URL pública temporária via Imgur.

## Meta Ads (campanhas pagas)

```bash
# Listar campanhas ativas
python3 {project-root}/.claude/skills/social-post-scheduler/scripts/meta_ads_client.py campaigns

# Ver métricas de uma campanha (últimos 30 dias)
python3 {project-root}/.claude/skills/social-post-scheduler/scripts/meta_ads_client.py insights <campaign_id>

# Criar campanha (inicia PAUSADA — ativar manualmente no Meta Business Suite)
python3 {project-root}/.claude/skills/social-post-scheduler/scripts/meta_ads_client.py create_campaign "<nome>" OUTCOME_TRAFFIC <budget_centavos> <start_iso> <end_iso>
```

## Output esperado

Após agendar, confirme com:
- Plataforma + conta
- Data/hora agendada (no fuso BRT)
- ID do post agendado
- Tipo de conteúdo (foto/carrossel)

## Notas
- Posts agendados ficam visíveis no Meta Business Suite em "Ferramentas de publicação → Posts agendados"
- A Meta exige agendamento com no mínimo 10 minutos de antecedência e no máximo 29 dias
- Stories não suportam agendamento via API — apenas feed e carrossel
- Credenciais ficam no `.env` na raiz do projeto
