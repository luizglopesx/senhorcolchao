---
tipo: snapshot-campanha
data_analise: 2026-07-07
fonte: Meta Ads API
campanha:
  nome: Durma como Campeão — Julho 2026 | CTWA
  id: 120247546410780752
  objetivo: OUTCOME_ENGAGEMENT (conversa no WhatsApp/Messenger)
  status: ACTIVE
  inicio_veiculacao: 2026-07-06
  fim_previsto: 2026-07-19
conjunto:
  nome: Fase 1 | Copa/Lançamento | 06-19/07 | R$30/dia
  id: 120247546410790752
  orcamento_diario: 30.00
  otimizacao: CONVERSATIONS
periodo_analisado: 2026-07-06 a 2026-07-07 (2 dias, campanha recém-lançada)
investimento_total: 28.66
conversas_iniciadas: 0
custo_por_conversa: null
metrica_resultado: onsite_conversion.messaging_conversation_started_7d
canais: [meta-ads]
---

# Snapshot — Durma como Campeão · Julho 2026 (2 dias)

> Dados da API em 07/07, campanha lançada em 06/07. Ainda cedo pra tirar conclusão — só 2 dias de veiculação.

## Números acumulados (06–07/jul)

| Métrica | Valor | Benchmark | Status |
|---|---|---|---|
| Investimento | R$ 28,66 | — | — |
| Alcance | 1.038 pessoas | — | — |
| Impressões | 1.733 | — | — |
| CTR | 0,35% | ≥ 0,95% | 🔴 abaixo |
| CPC (link) | R$ 4,78 | ≤ R$ 3 | 🔴 acima |
| CPM | R$ 16,54 | ≤ R$ 13 | 🔴 acima |
| Cliques no link | 1 | — | — |
| Conversas iniciadas (7d) | 0 | custo ≤ R$ 11 | ainda sem conversão |

## Engajamento orgânico

| Ação | Valor |
|---|---|
| Interações na página | 244 |
| Video views | 240 |
| Curtidas | 1 |
| Interações no post | 3 |

Bastante engajamento (vídeo, curtida) mas quase nenhum clique real e zero conversa iniciada até agora.

## Leitura

- 🟡 Ainda é só o 2º dia — não dá pra decidir nada com esse volume de dado
- 🔴 CTR, CPC e CPM já vieram piores que o padrão histórico (comparado a Namorados/CP04)
- 🔴 Objetivo é conversa no WhatsApp, mas resultado até agora é engajamento orgânico (vídeo/curtida), não conversa
- 📅 Reavaliar em 2-3 dias — se continuar sem conversa e CTR baixo até dia 09-10/07, considerar revisar criativo ou segmentação

## Causa provável identificada e corrigida (07/07, mesmo dia)

O conjunto estava com um público lookalike **"LAL 1% | Leads Copa | Brasil | Julho 2026"** empilhado sobre geo (Barretos 40km) + idade + interesses.

- Base de origem ("BASE | Leads Copa | Junho/Julho 2026") = ~300 contatos enviados, aparecendo na Meta com tamanho estimado de apenas **~1.000 pessoas** (piso mínimo de exibição)
- O lookalike 1% gerado a partir dela também aparecia com **~1.000 pessoas** — muito abaixo do normal pra um LAL 1% de Brasil (que costuma ficar na casa das centenas de milhares/milhões)
- Base de origem pequena demais (300 contatos, abaixo do mínimo recomendado pela Meta de ~1.000) resultou num lookalike raso, sem sinal suficiente pra expandir de verdade
- Combinado com geo + interesse + idade, a sobreposição elegível ficava minúscula — reach de 1.038 pessoas em 2 dias já batia quase no teto do público disponível, explicando CTR baixo, CPM alto e zero conversa

**Ação:** Luiz removeu o público lookalike do conjunto em 07/07. Segmentação atual: Barretos 40km + idade 25-55 + interesses (Móveis, Decoração, Colchão, Recently moved), sem custom audience.

**Próximo passo:** acompanhar reach/CTR/CPM nos próximos 2-3 dias pra confirmar se a remoção destravou o alcance. Pra próxima base de lookalike, juntar bem mais contatos antes de gerar (mínimo 1.000, ideal 3-5 mil).
