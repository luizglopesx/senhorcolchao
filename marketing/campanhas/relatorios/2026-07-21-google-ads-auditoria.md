---
tipo: auditoria-campanhas
data_analise: 2026-07-21
fonte: Google Ads API v21
canais: [google-ads]
campanhas_ativas: [CP01C]
---

# Auditoria Google Ads — 21/07/2026

## Contexto

Checagem de rotina, mesmo racional das auditorias anteriores.

## Achado 1 — Situação da campanha ativa (14 dias)

| Campanha | Status | Orçamento | Gasto 14d | Cliques | Conversões |
|---|---|---|---|---|---|
| CP01C (Search) | ENABLED | R$25/dia | R$ 333,70 | 145 | 12 |

Demais campanhas seguem PAUSED, sem gasto — só CP01C teve custo nos últimos 7 dias.

CPA médio 14d da CP01C: **R$ 27,81** — estável no mesmo patamar bom da checagem anterior (R$27,69).

## Achado 2 — Dia a dia (14 a 20/07)

| Data | Cliques | Gasto | Conversões |
|---|---|---|---|
| 14/07 | 13 | R$ 22,95 | 4 |
| 15/07 | 9 | R$ 24,85 | 1 |
| 16/07 | 11 | R$ 23,79 | 2 |
| 17/07 | 5 | R$ 17,80 | 2 |
| 18/07 | 10 | R$ 16,70 | 0 |
| 19/07 | 7 | R$ 15,77 | 0 |
| 20/07 | 15 | R$ 24,52 | **1** |

A pausa de conversão do fim de semana (18-19/07) quebrou em 20/07 com 1 conversão nova — confirma que era só variação de volume de fim de semana, não vazamento.

## Achado 3 — Meta Ads: Durma como Campeão desativada manualmente

O usuário desativou manualmente a campanha "Durma como Campeão" no Meta Ads hoje — ela seguia com status `ACTIVE` no objeto (mesmo sem gastar desde 19/07) porque não tinha sido arquivada. Confirmado que campanhas ativas no Meta agora são só **Pré-Festa do Peão** e **Venda Lotes de Terreno** (negócio à parte, não é da Senhor Colchão).

## Ações recomendadas

1. **Nenhuma ação hoje no Google Ads.** CPA estável, situação saudável.
2. Continuar sem criar campanha nova.
3. Próxima checagem sob demanda.
