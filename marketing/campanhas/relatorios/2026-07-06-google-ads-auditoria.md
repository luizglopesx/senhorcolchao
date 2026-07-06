---
tipo: auditoria-campanhas
data_analise: 2026-07-06
fonte: Google Ads API v21
canais: [google-ads]
campanhas_ativas: [CP01C, CP02A]
---

# Auditoria Google Ads — 06/07/2026

## Contexto

Usuário reportou a primeira conversão real de `whatsapp_click` desde a correção do gclid (03–04/07). Auditoria pra confirmar o dado, checar saúde geral da conta (keywords, negativas) e avaliar se cabe criar campanha nova.

## Achado 1 — Conversão confirmada, com dado real da API

**1 conversão `whatsapp_click` em 05/07/2026, na campanha CP01C.** Confirmado via `conversion_action` que a ação está `ENABLED`, categoria `CONTACT`, `primaryForGoal = true` — segue tudo certo do lado de configuração. Fecha o ciclo: gclid chega intacto (confirmado 04/07) → clique atribuído (GA4, 04/07) → agora conversão de fato contabilizada no Google Ads (05/07).

**Nota sobre atraso de relatório:** essa conversão ainda não aparece nos relatórios de keyword/search term (normal — o Google Ads costuma levar de algumas horas a 1–2 dias pra propagar conversão pros relatórios de granularidade mais fina). Não é motivo de alarme.

## Achado 2 — Situação geral das campanhas ativas (14 dias)

| Campanha | Status | Orçamento | Gasto 14d | Cliques | Conversões |
|---|---|---|---|---|---|
| CP01C (Search) | ENABLED | R$25/dia | R$270,81 | 97 | 1 |
| CP02A (Display Rmkt) | PAUSED | R$5/dia | R$53,07 (histórico, antes da pausa) | 88 | 0 |

CP01C está gastando em média R$19,34/dia — **abaixo** do teto de R$25. Diferente do achado de 03/07 (orçamento estourando quase todo dia), agora sobra espaço de orçamento. Bom sinal: não é mais o orçamento que está limitando a campanha.

## Achado 3 — Problema real encontrado: 1 keyword broad consumindo mais da metade do orçamento, zero conversão

**"Comprar colchão de espuma" (BROAD, grupo "Colchões De Espuma")**: R$141,97 gastos em 14 dias — **52% de todo o gasto da CP01C** — 24 cliques, 375 impressões, **zero conversões**.

Como é broad match, essa keyword está disparando pra buscas bem mais amplas do que o produto: "cama box casal", "colchão casal", "colchão d33 king", "cama king casal", "colchões pikolin" (marca concorrente), "colchão kenko light" (marca concorrente) — nenhuma converteu.

Isso é exatamente o mesmo padrão de vazamento que a auditoria de 03/07 já tinha corrigido no grupo Branding (lá era "colchoes barretos" em broad → migrada pra phrase). Aqui é o mesmo problema, keyword diferente, grupo diferente.

## Achado 4 — Negativas: lacunas pontuais encontradas

Lista "02 - Concorrentes" (24 termos) já cobre a maioria das marcas concorrentes (Castor, Ortobom variantes, Casas Bahia, etc.) e "doctor colchões" e "colchão kenko" já estão bloqueados a nível de campanha. Mas nos termos de pesquisa reais dos últimos 30 dias, dois termos de concorrente **ainda não bloqueados** geraram custo sem conversão:

- **"colchões pikolin"** — R$6,76, marca concorrente (Pikolin), não está em nenhuma lista de negativas
- **"colchões vitorian"** — R$4,37 (dentro do total, aparece no relatório de termos), marca não identificada nas listas atuais

O restante do gasto sem conversão (R$0,50–R$16 cada) é ruído normal de long-tail em conta pequena — não justifica negativar termo a termo, melhor resolvido corrigindo o match type (achado 3).

## Ações recomendadas

1. **Migrar "Comprar colchão de espuma" de BROAD para PHRASE** no grupo "Colchões De Espuma" — mesma lógica já aplicada em 03/07 no grupo Branding. Deve cortar a maior fonte de gasto sem retorno da conta.
2. **Adicionar "pikolin" e "vitorian" à lista de negativas "02 - Concorrentes"** — gasto pequeno, mas zero chance de converter (concorrentes).
3. **Não criar campanha nova agora.** Motivos:
   - Só 1 conversão registrada, 1 dia de dado "limpo" depois do fix — estatisticamente não dá pra tirar conclusão nenhuma ainda (a própria estratégia já previa esperar 2–4 semanas de dado limpo antes de decidir sobre alocação de verba)
   - Tem orçamento sobrando na campanha atual (R$25/dia com gasto médio de R$19,34) — antes de criar campanha nova, faz mais sentido aproveitar esse espaço consertando o vazamento do achado 3
   - Foco definido em `_memoria/estrategia.md` é a campanha **Durma como Campeão** (julho) — Google Ads aqui é canal secundário, ainda em fase de estabilização de tracking
4. **Continuar monitorando** — próxima checagem de CPL real (custo ÷ conversões) faz sentido em ~2 semanas, quando a conversão de 05/07 tiver decantado nos relatórios e (espera-se) mais conversões tiverem entrado.

## Ações executadas (via API, 06/07/2026)

| Ação | Resultado |
|---|---|
| "Comprar colchão de espuma" migrada de BROAD → PHRASE (grupo "Colchões De Espuma", CP01C) | ✅ Aplicado — broad original removida (`REMOVED`), nova phrase `ENABLED`. Confirmado via API pós-alteração |
| "pikolin" e "vitorian" adicionadas à lista de negativas "02 - Concorrentes" (PHRASE) | ✅ Aplicado — confirmado via API, 2 novos `sharedCriteria` criados |

**Efeito esperado:** a migração pra phrase reabre revisão de política do anúncio associado (normal, minutos a horas). Deve cortar o vazamento de ~R$142/14 dias em buscas genéricas/concorrentes, liberando mais do orçamento diário (R$25) pra tráfego com intenção mais próxima do produto.

## Pendências já conhecidas (sem mudança nesta auditoria)

- Resposta da hospedagem (OpsEmpresas) sobre o redirect www → sem-www ainda pendente
- CP02B/CP03A seguem como estavam (pausada / removida) — nenhuma ação necessária
