---
tipo: auditoria-campanhas
data_analise: 2026-07-07
fonte: Google Ads API v21
canais: [google-ads]
campanhas_ativas: [CP01C, CP02A]
---

# Auditoria Google Ads — 07/07/2026

## Contexto

Checagem de rotina, seguindo a correção aplicada na auditoria de 06/07 (broad → phrase em "Comprar colchão de espuma" + negativas "pikolin"/"vitorian").

## Achado 1 — Segunda conversão real confirmada, dias consecutivos

`whatsapp_click` disparou em **05/07 E 06/07** (1 conversão em cada dia) — CP01C acumula agora **2 conversões em 14 dias**, contra 1 na auditoria anterior. Ainda é pouco dado pra tirar CPL de verdade, mas é o segundo dia seguido com conversão real desde a correção do gclid — sinal positivo de continuidade.

## Achado 2 — Situação das campanhas ativas (14 dias)

| Campanha | Status | Orçamento | Gasto 14d | Cliques | Conversões |
|---|---|---|---|---|---|
| CP01C (Search) | ENABLED | R$25/dia | R$267,60 | 94 | 2 |
| CP02A (Display Rmkt) | PAUSED | R$5/dia | R$48,21 (histórico) | 84 | 0 |

Gasto médio de CP01C segue abaixo do teto (~R$19/dia de R$25) — segue sobrando orçamento, não é mais fator limitante.

## Achado 3 — Correção de 06/07 confirmada, efeito ainda cedo pra medir

- **"Comprar colchão de espuma" (BROAD)** confirmado `REMOVED` — só restou o gasto residual de antes da troca no próprio dia 06/07 (R$10,01, 3 cliques, 1 conversão, antes da migração ter efeito)
- **Versão PHRASE** nova: só 2 impressões, 0 clique, 0 gasto desde a troca — tempo insuficiente pra avaliar se o vazamento parou de verdade. Reavaliar em 3-5 dias
- **Negativas "pikolin" e "vitorian"** confirmadas na lista "02 - Concorrentes" (`sharedCriterion` ativo) — a alteração se manteve

## Achado 4 — Dia de hoje (parcial)

07/07 até o momento da checagem: R$1,77 gastos, 2 cliques, 7 impressões, 0 conversão. Normal pra início de dia, nada fora do padrão.

## Nenhum vazamento novo encontrado

Top keywords por gasto no período seguem sem surpresas — nenhuma keyword nova queimando orçamento sem conversão além do que já estava mapeado.

## Ações recomendadas

1. **Nenhuma ação corretiva necessária hoje** — a correção de 06/07 está de pé, só precisa de mais dias de dado pra confirmar o efeito completo na keyword migrada
2. **Continuar sem criar campanha nova** — mesmo racional da auditoria anterior: só 2 conversões acumuladas, foco segue em Meta Ads (Durma como Campeão)
3. **Próxima checagem:** em 3-5 dias, quando a versão phrase de "Comprar colchão de espuma" tiver volume suficiente pra avaliar se cortou o vazamento
