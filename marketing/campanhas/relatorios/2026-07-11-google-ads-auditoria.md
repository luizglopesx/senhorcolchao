---
tipo: auditoria-campanhas
data_analise: 2026-07-11
fonte: Google Ads API v21
canais: [google-ads]
campanhas_ativas: [CP01C, CP02A]
---

# Auditoria Google Ads — 11/07/2026

## Contexto

Checagem de rotina + verificação específica pedida pelo usuário: "palavras ainda certas? palavras negativas?" — conferir se as keywords seguem saudáveis e se a lista de negativas segue funcionando desde a correção de 06/07.

## Achado 1 — Situação das campanhas ativas (14 dias)

| Campanha | Status | Orçamento | Gasto 14d | Cliques | Conversões |
|---|---|---|---|---|---|
| CP01C (Search) | ENABLED | R$25/dia | R$301,87 | 89 | 3 |
| CP02A (Display Rmkt) | PAUSED | R$5/dia | R$28,72 (histórico) | 59 | 0 |

## Achado 2 — Dia a dia de CP01C (09 a 11/07)

| Data | Cliques | Gasto | Conversões |
|---|---|---|---|
| 09/07 | 7 | R$26,48 | 1 |
| 10/07 | 5 | R$26,46 | 0 |
| 11/07 (parcial) | 1 | R$2,82 | 0 |

1 dia sem conversão (10/07) é variação normal pro volume da conta, não é vazamento.

## Achado 3 — Verificação de keywords e negativas (pedido explícito do usuário)

Termos de busca reais desde a correção de 06/07 (07/07 a 11/07), toda a campanha:

| Termo | Gasto | Grupo | Keyword |
|---|---|---|---|
| casa dos colchões | R$6,97 | Branding | EXACT (esperado, marca própria) |
| colchão solteiro d20 88x188 | R$4,65 | Colchões De Espuma | PHRASE migrada, no assunto |
| loja de colchões barretos | R$4,46 | Branding | PHRASE (esperado) |
| cama de casal box | R$1,35 | Cama Box Molas | BROAD |
| ventas de camas cerca de mi | R$1,32 | Cama Box Molas | BROAD (espanhol, baixo custo) |

**Negativas confirmadas funcionando:** "pikolin" e "vitorian" (adicionadas em 06/07) não aparecem mais nos termos de busca desde a correção — bloqueio efetivo. A keyword broad antiga "Comprar colchão de espuma" segue `REMOVED`, sem gasto novo desde a migração.

**Conclusão:** nenhum vazamento novo. Toda atividade de custo mais alto que aparece no lookback de 14 dias (ex: "colchao barretos" R$15,02, "colchões pikolin" R$6,76) é **histórica, anterior à correção de 06/07** — já tratada, não é problema atual.

## Ações recomendadas

1. **Nenhuma ação hoje.** Keywords e negativas seguem saudáveis.
2. Continuar sem criar campanha nova — mesmo racional das auditorias anteriores
3. Próxima checagem sob demanda
