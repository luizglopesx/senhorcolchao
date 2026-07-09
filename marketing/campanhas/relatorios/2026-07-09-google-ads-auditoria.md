---
tipo: auditoria-campanhas
data_analise: 2026-07-09
fonte: Google Ads API v21
canais: [google-ads]
campanhas_ativas: [CP01C, CP02A]
---

# Auditoria Google Ads — 09/07/2026

## Contexto

Checagem de rotina. CP01C ficou 2 dias seguidos (07/07 e 08/07) sem conversão, gastando perto do teto diário — investigado pra descartar vazamento novo.

## Achado 1 — Situação das campanhas ativas (14 dias)

| Campanha | Status | Orçamento | Gasto 14d | Cliques | Conversões |
|---|---|---|---|---|---|
| CP01C (Search) | ENABLED | R$25/dia | R$301,19 | 106 | 2 |
| CP02A (Display Rmkt) | PAUSED | R$5/dia | R$38,35 (histórico) | 74 | 0 |

## Achado 2 — Dia a dia de CP01C (06 a 09/07)

| Data | Cliques | Gasto | Conversões |
|---|---|---|---|
| 06/07 | 9 | R$23,08 | 1 |
| 07/07 | 13 | R$26,65 | 0 |
| 08/07 | 9 | R$26,58 | 0 |
| 09/07 (parcial) | 1 | R$1,35 | 0 |

## Achado 3 — Investigado: sem vazamento estrutural novo

Dois dias seguidos sem conversão gastando perto do teto (~R$25/dia) acendeu alerta — mesmo padrão do achado anterior (keyword broad sozinha consumindo >50% do orçamento). Desta vez **não é o caso**: o gasto de 07-09/07 está distribuído entre 5+ keywords diferentes, cada uma com 1-3 cliques:

| Keyword | Match | Gasto (3d) | Cliques |
|---|---|---|---|
| Promoção cama box espuma casal | BROAD | R$13,37 | 1 |
| Comprar colchão de espuma | PHRASE (migrada) | R$12,43 | 3 |
| Colchão de molas ensacadas | BROAD | R$9,64 | 2 |
| colchões em barretos | PHRASE | R$4,54 | 2 |
| Cama Box Molas Promoção | BROAD | R$1,35 | 1 |

Nenhuma keyword dominando sozinha. Com a conta fazendo ~2 conversões a cada 14 dias (taxa baixa e rara), 2 dias seguidos sem conversão é variação estatística normal, não indício de vazamento — diferente do caso anterior onde 52% do orçamento ia pra uma única keyword genérica.

A keyword migrada ("Comprar colchão de espuma" → phrase) segue limpa: R$12,43 acumulados, 3 cliques, 0 conversão ainda — volume baixo demais pra julgar.

## Ações recomendadas

1. **Nenhuma ação hoje.**
2. **Ponto de atenção:** se passar mais 2-3 dias sem nenhuma conversão nova, reabrir auditoria de keyword a fundo (procurar vazamento estrutural, não só variação normal)
3. Continuar sem criar campanha nova — mesmo racional das auditorias anteriores
