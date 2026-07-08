---
tipo: auditoria-campanhas
data_analise: 2026-07-08
fonte: Google Ads API v21
canais: [google-ads]
campanhas_ativas: [CP01C, CP02A]
---

# Auditoria Google Ads — 08/07/2026

## Contexto

Checagem de rotina, acompanhando o efeito da migração broad → phrase em "Comprar colchão de espuma" (aplicada em 06/07, primeira leitura em 07/07).

## Achado 1 — Situação das campanhas ativas (14 dias)

| Campanha | Status | Orçamento | Gasto 14d | Cliques | Conversões |
|---|---|---|---|---|---|
| CP01C (Search) | ENABLED | R$25/dia | R$285,12 | 104 | 2 |
| CP02A (Display Rmkt) | PAUSED | R$5/dia | R$43,15 (histórico) | 80 | 0 |

Nenhuma conversão nova desde 06/07 (segue em 2 acumuladas nos 14 dias) — nada caiu, mas nada subiu hoje também.

## Achado 2 — Dia a dia de CP01C (06 a 08/07)

| Data | Cliques | Gasto | Conversões |
|---|---|---|---|
| 06/07 | 9 | R$23,08 | 1 |
| 07/07 | 14 | R$27,63 | 0 |
| 08/07 (parcial) | 1 | R$2,88 | 0 |

## Achado 3 — Migração broad → phrase confirmada funcionando

Comparei os termos de busca reais que dispararam a keyword "Comprar colchão de espuma" desde a troca (06–08/07):

**Antes (BROAD, atividade residual do próprio dia 06/07 antes da troca):** "olx colchão casal", "zema cama box", "box bau casal", "cama de viúva box", "loja de colchões perto de mim" — buscas amplas, fora do produto específico, sem conversão (exceto 1 conversão em "sono prime colchões", R$5,35, provavelmente já convertida antes do corte)

**Depois (PHRASE, 2 dias de vida):** "colchão solteiro d20 88x188", "colchão casal d33", "colchão casal espuma", "colchão densidade 33", "colchão queen espuma d45 ortobom" — buscas específicas de colchão, no assunto. R$12,43 gastos, 3 cliques, 0 conversão ainda (pouco volume pra julgar CPL, mas qualidade do termo mudou completamente)

**Conclusão:** a correção funcionou como esperado — parou de vazar pra buscas de marketplace/concorrente genérico e passou a servir só termos de colchão. Ainda cedo pra medir conversão da keyword nova isoladamente.

## Achado 4 — Nenhum vazamento novo

Negativas "pikolin" e "vitorian" seguem ativas. Nenhuma keyword nova consumindo orçamento sem conversão fora do que já estava mapeado.

## Ações recomendadas

1. **Nenhuma ação hoje.** Migração se provou correta pelos termos de busca; falta só volume pra confirmar CPL da keyword phrase
2. Continuar sem criar campanha nova — mesmo racional das auditorias anteriores
3. Próxima checagem sob demanda, como de costume
