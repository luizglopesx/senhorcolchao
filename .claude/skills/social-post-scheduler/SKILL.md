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

### Campanha CTWA completa (WhatsApp) — pausada, pronta pra revisão

Fluxo padrão de 6 comandos pra montar campanha → ad set → criativo → anúncio via API. Comprovado em 17/07/2026 com a campanha Pré-Festa do Peão. Ver memória `meta-ads-ctwa-workflow` pro histórico completo.

```bash
SCRIPT={project-root}/.claude/skills/social-post-scheduler/scripts/meta_ads_client.py

# 1. Campanha CTWA (sem orçamento no nível campanha — orçamento fica no ad set)
python3 $SCRIPT create_campaign_ctwa "<nome>" <start_iso-0300> <end_iso-0300>

# 2. Ad set — targeting_json_file tem geo_locations.cities (raio) + flexible_spec.interests
python3 $SCRIPT create_ad_set_full <campaign_id> "<nome>" <budget_centavos> <start> <end> <targeting_json_file>

# 3. Upload do vídeo (só formato feed — o Meta corta sozinho pra Stories/Reels, ver ressalva abaixo)
python3 $SCRIPT upload_video <file_path.mp4> "<nome>"   # retorna video_id

# 4. Upload da thumbnail (obrigatória)
python3 $SCRIPT upload_image <file_path.png>             # retorna image_hash

# 5. Criativo — CTA WHATSAPP_MESSAGE + mensagem de boas-vindas pré-preenchida
python3 $SCRIPT create_video_creative <video_id> "<nome>" "<title>" "<message>" "<link_description>" "<intro_text>" "<autofill_message>" <image_hash>

# 6. Anúncio (vincula criativo ao ad set)
python3 $SCRIPT create_ad "<nome>" <ad_set_id> <creative_id>
```

**Só precisa do motion em formato feed** — o Meta gera sozinho a versão cortada pra Stories/Reels (confirmado pela campanha ativa de melhor CTR da conta, que usa esse exato padrão). Formato story continua necessário pro orgânico, mas ali usa imagem estática, não motion.

**Nomeação de arquivo:** ao subir vídeos manualmente na Biblioteca de Mídia, nomear com o produto (ex: `d28-solteiro-feed.mp4`) — nomes genéricos tipo `motion-feed.mp4` repetidos em várias pastas impedem identificar o `video_id` certo depois.

**Armadilhas já resolvidas:**
- Campanha CTWA sem orçamento próprio precisa de `is_adset_budget_sharing_enabled` explícito
- `bid_strategy: LOWEST_COST_WITHOUT_CAP` vai no **ad set**, não na campanha (senão a Meta exige `bid_amount`)
- `create_video_creative` exige `image_hash` (thumbnail) — sem isso a Meta rejeita o criativo

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
