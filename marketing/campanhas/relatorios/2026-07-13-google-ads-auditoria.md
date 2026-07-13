---
tipo: auditoria-campanhas
data_analise: 2026-07-13
fonte: Google Ads API v21
canais: [google-ads]
campanhas_ativas: [CP01C, CP02A]
---

# Auditoria Google Ads — 13/07/2026

## Contexto

Checagem de rotina + aprofundamento pedido pelo usuário (mesmo racional das auditorias anteriores): conferir situação das campanhas ativas e revalidar se as negativas de concorrentes ("pikolin", "vitorian") seguem funcionando desde a correção de 06/07.

## Achado 1 — Situação das campanhas ativas (14 dias)

| Campanha | Status | Orçamento | Gasto 14d | Cliques | Conversões |
|---|---|---|---|---|---|
| CP01C (Search) | ENABLED | R$25/dia | R$ 325,10 | 108 | 4 |
| CP02A (Display Rmkt) | PAUSED | R$5/dia | R$ 19,06 (residual) | 39 | 0 |

Demais campanhas (CP04A/B PMax, 001.01, CP02B) seguem PAUSED, sem gasto nem impressão no período.

CPA médio 14d da CP01C: R$ 81,27 — melhora frente ao R$ 100,62 do relatório de 11/07.

## Achado 2 — Dia a dia de CP01C (06 a 12/07)

| Data | Cliques | Gasto | Conversões |
|---|---|---|---|
| 06/07 | 9 | R$ 23,08 | 1 |
| 07/07 | 13 | R$ 26,65 | 0 |
| 08/07 | 9 | R$ 26,58 | 0 |
| 09/07 | 7 | R$ 26,48 | 1 |
| 10/07 | 5 | R$ 26,46 | 0 |
| 11/07 | 9 | R$ 24,96 | 0 |
| 12/07 | 20 | R$ 27,64 | 1 |

Pacing estável, sempre próximo do orçamento diário (R$25). 12/07 foi o melhor dia do período (20 cliques, 665 impressões, 1 conversão). Dias sem conversão são variação normal pro volume da conta, não indicam vazamento.

## Achado 3 — Verificação de keywords e negativas (aprofundamento pedido pelo usuário)

Termos de busca reais no período 07/07–13/07 (CP01C), toda a campanha:

| Termo | Gasto | Grupo | Keyword casada |
|---|---|---|---|
| casa dos colchões | R$ 6,97 | Branding | EXACT (marca própria) |
| colchão solteiro d20 88x188 | R$ 4,65 | Colchões De Espuma | PHRASE migrada, no assunto |
| loja de colchões barretos | R$ 4,46 | Branding | PHRASE (esperado) |
| colchão | R$ 2,17 | Colchões De Espuma | BROAD — genérico, custo trivial |
| cama de casal box | R$ 1,35 | Cama Box Molas | BROAD |
| ventas de camas cerca de mi | R$ 1,32 | Cama Box Molas | BROAD (espanhol, baixo custo) |

**Negativas de concorrentes confirmadas ativas:** consultado direto na lista compartilhada "02 - Concorrentes" (vinculada à CP01C, status ENABLED) — "pikolin" e "vitorian" (adicionadas em 06/07) seguem cadastradas e ENABLED. Nenhum dos dois termos aparece nos termos de busca reais do período — bloqueio efetivo.

**Migração da keyword antiga confirmada:** a keyword BROAD "Comprar colchão de espuma" está `REMOVED`. A versão PHRASE com o mesmo texto está `ENABLED` e é quem responde pelo termo "colchão solteiro d20 88x188" — consistente com a correção de 06/07.

**Outras listas de negativas ativas na campanha:** "01 - Padrão", "03 - Grátis", "04 - Cidades" — todas ENABLED, sem alteração.

**Conclusão:** nenhum vazamento novo, nenhuma negativa caiu ou foi removida. Único ponto de atenção menor: termo genérico "colchão" (BROAD, R$2,17) — custo baixo, não urgente.

## Ações recomendadas

1. **Nenhuma ação urgente hoje.** Keywords e negativas seguem saudáveis, CPA melhorando.
2. **Opcional:** adicionar "colchão" como negativa EXACT no grupo Colchões De Espuma, já que a keyword BROAD "Colchão de espuma preço" deveria cobrir sozinha essa intenção.
3. Continuar sem criar campanha nova — mesmo racional das auditorias anteriores.
4. Próxima checagem sob demanda.
