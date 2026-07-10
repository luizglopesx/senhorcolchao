---
tipo: auditoria-campanhas
data_analise: 2026-07-10
fonte: Google Ads API v21
canais: [google-ads]
campanhas_ativas: [CP01C, CP02A]
---

# Auditoria Google Ads — 10/07/2026

## Contexto

Checagem de rotina. Segue o ponto de atenção da auditoria de 09/07 (2 dias seguidos sem conversão) — checar se resolveu ou virou vazamento.

## Achado 1 — Situação das campanhas ativas (14 dias)

| Campanha | Status | Orçamento | Gasto 14d | Cliques | Conversões |
|---|---|---|---|---|---|
| CP01C (Search) | ENABLED | R$25/dia | R$297,82 | 92 | 3 |
| CP02A (Display Rmkt) | PAUSED | R$5/dia | R$32,73 (histórico) | 62 | 0 |

## Achado 2 — Terceira conversão real confirmada, alerta anterior resolvido

`whatsapp_click` disparou em **09/07** — confirmado via API (`conversionActionName`). O ponto de atenção levantado ontem (2 dias seguidos sem conversão) se resolveu naturalmente, como esperado: era variação estatística normal, não vazamento estrutural.

## Achado 3 — Dia a dia de CP01C (07 a 10/07)

| Data | Cliques | Gasto | Conversões |
|---|---|---|---|
| 07/07 | 13 | R$26,65 | 0 |
| 08/07 | 9 | R$26,58 | 0 |
| 09/07 | 7 | R$26,48 | **1** |
| 10/07 (parcial) | 1 | R$2,98 | 0 |

## Achado 4 — Keyword migrada segue sem mudança

"Comprar colchão de espuma" (PHRASE, migrada em 06/07): R$12,43 acumulados, 3 cliques, 0 conversão — mesmos números do dia anterior, sem atividade nova. A conversão de 09/07 veio de outra keyword/grupo, não afeta a leitura desta migração. Ainda cedo/pouco volume pra julgar CPL isolado dela.

## Ações recomendadas

1. **Nenhuma ação hoje.**
2. Encerrado o ponto de atenção da auditoria anterior — 3 conversões em 14 dias, tendência normal pro volume da conta
3. Continuar sem criar campanha nova — mesmo racional das auditorias anteriores
4. Próxima checagem sob demanda
