---
tipo: relatorio-atendimentos
data_analise: 2026-07-01
fonte: Campaign Manager API
periodo: 2026-06-15 a 2026-06-30
canais: [whatsapp, campaign-manager]
---

# Atendimentos — Campaign Manager · 15–30/jun/2026

> Período da campanha Meta Ads Copa 2026. Cruzamento entre leads gerados pelo Meta e tratamento no CM.

---

## Volume de conversas

| Métrica | Valor |
|---|---|
| Conversas com atividade no período | **193** (60 abertas + 133 arquivadas) |
| Conversas novas geradas pelo Meta Ads (Copa) | 63 |
| Mensagens de follow-up automático enviadas | **313** |
| Tempo médio de primeira resposta | **4 minutos** 🟢 |
| Taxa de resposta dos leads | 27,6% |

---

## Funil de atendimento (acumulado)

| Estágio | Contatos |
|---|---|
| Ativos (em conversa) | 68 |
| Responderam | 94 |
| Completados | 135 |
| Pausados | 43 |

---

## Follow-ups automáticos por dia (15–30/jun)

| Dia | Mensagens enviadas |
|---|---|
| 15/jun (seg) | 36 |
| 16/jun (ter) | 21 |
| 17/jun (qua) | 26 |
| 18/jun (qui) | 24 |
| 19/jun (sex) | 24 |
| 20–21/jun (fim de semana) | 0 |
| 22/jun (seg) | 19 |
| 23/jun (ter) | 34 |
| 24/jun (qua) | 11 |
| 25/jun (qui) | 32 |
| 26/jun (sex) | 28 |
| 27–28/jun (fim de semana) | 0 |
| 29/jun (seg) | **39** (pico) |
| 30/jun (ter) | 19 |
| **Total** | **313** |

Padrão claro: follow-ups param nos fins de semana (sáb/dom). Pico na segunda-feira após o fim de semana.

---

## Inbound por dia da semana (última semana, 25/jun–01/jul)

| Dia | Mensagens recebidas |
|---|---|
| Quinta (25/jun) | 71 |
| Sexta (26/jun) | 55 |
| Sábado (27/jun) | 23 |
| Domingo (28/jun) | 27 |
| Segunda (29/jun) | **81** 🟢 (pico da semana) |
| Terça (30/jun) | 73 |
| Quarta (01/jul) | 47 |

Segunda é o dia de maior inbound — leads que pensaram no fim de semana e voltam na segunda.

---

## Alerta: disparo Copa 2026 dentro do CM

A campanha **"Copa 2026 — Pré-jogo Escócia vs Brasil"** criada no Campaign Manager teve **100% de falha**:
- 2.103 destinatários
- 0 entregues
- Causa provável: número de WhatsApp bloqueado / limite de disparos em massa

Esse resultado puxa a taxa de falha geral do período para 80,7%, mas não reflete a saúde real dos follow-ups (715 enviados, 1 falha — taxa de sucesso >99%).

**Ação recomendada:** verificar status do número e limite de disparos antes de tentar novo broadcast em massa.

---

## Conversas paradas — atenção imediata

| Contato | Parada há | Intenção | Situação |
|---|---|---|---|
| Patricia Alves | ~54h | Produto/Medida | Perguntou sobre cama box Queen |
| fabi 🌻🌈 | ~41h | — | Pediu mais informações |
| Creusina Bosso | ~32h | Produto/Medida | 🔴 **Objeção**: "vou ter que esperar um pouco pra comprar" |
| Zoraida Fares | ~30h | Preço | "Quero saber valores. Bom dia, depois eu vou aí." |
| Luís Carlos | ~22h | Entrega | 🔴 **Objeção**: atraso no dobro do prazo combinado |

**Luís Carlos** é urgente — cliente reclamando de entrega com prazo dobrado. Risco de avaliação negativa.

---

## Cruzamento Meta Ads × Campaign Manager

| Dimensão | Meta Ads (Copa) | Campaign Manager |
|---|---|---|
| Leads novos gerados | 63 conversas | — |
| Conversas tratadas no período | — | 193 |
| Custo por lead novo | R$ 9,27 | — |
| Automação ativa | — | 313 follow-ups enviados |
| Tempo 1ª resposta | — | 4 minutos |
| Taxa de resposta | 90% (5+ trocas: 48%) | 27,6% (base total) |

O CM processou 3× mais conversas do que o Meta gerou — inclui base antiga sendo reativada via follow-up junto com os leads novos da Copa.

---

## Principal ponto de atenção

**priceSilenceCount: 32** — 32 leads receberam o preço e não responderam mais. Equivale a ~50% das novas conversas da Copa. Possíveis causas:

1. Preço apresentado sem contexto/valor (só número, sem ancoragem)
2. Sem oferta de facilidade (parcelamento, frete, prazo)
3. Sem follow-up após o envio do preço

**Recomendação:** revisar o script de atendimento no ponto de envio de preço — incluir parcelamento e CTA de visita ou próximo passo claro.
