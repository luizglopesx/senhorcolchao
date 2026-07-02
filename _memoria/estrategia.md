# Estratégia

## Fase

Operação estabilizada — caixa controlado, equipe formada. Faturamento batendo meta em junho (R$185.823 vs meta R$180.000), mas lucro líquido comprimido pelos custos fixos altos.

## Prioridade principal

**Manter faturamento acima da meta e reduzir custos fixos proporcionais.** O gargalo em junho não foi venda — foi que os custos fixos (36,2% da receita, teto 25,2%) consumiram toda a margem. Pró-labore sozinho representa 14,3% da receita. Lucro líquido foi 0,77% (meta: 10%). DRE completo: `marketing/campanhas/relatorios/2026-07-01-dre-junho-2026.md`

## O que pode esperar

- Expansão de equipe
- Novos produtos / categorias
- Reformas estruturais

## Contexto com prazo

- Ações imediatas: promoções e campanhas para girar estoque (sem prazo fixo — até o estoque normalizar)

## Campanhas ativas (2026)

- *(Nenhuma campanha de prospecção ativa em julho/2026 — Copa encerrou em 30/jun)*

## Campanhas encerradas (referência)

- **Copa 2026** ✅ encerrada 30/jun — 63 conversas, R$9,27/conversa. Relatório: `marketing/campanhas/relatorios/2026-06-30-aqui-da-jogo-copa-encerramento.md`
- **Dia dos Namorados 2026** ✅ encerrada 13/jun — 50 conversas, R$10,82/conversa
- **Bota Fora Maio 2026** ✅ encerrada — campanha em `marketing/campanhas/bota-fora-maio-2026/`

## Frentes em andamento

- **Redesign de páginas de produto no Simplo 7** — layout HTML padronizado definido e aprovado. Páginas organizadas por produto em `saidas/produtos/<produto>/`. Primeiro produto (**Livorno**) finalizado: mockup com fotos fotorrealistas (hero/colchão/base) em `saidas/produtos/livorno/mockup-livorno.html`, código pronto pra colar no Simplo 7 em `descricao-simplo7.html` e imagens otimizadas em `web/`. Pendente: hospedar as imagens no Simplo 7 e colar o código no catálogo

## Benchmarks de mídia paga — Meta Ads

Referências pra avaliar campanhas novas (objetivo engajamento → conversa no WhatsApp/Messenger). Atualizar conforme novas campanhas rodarem.

| Métrica | Meta / referência | Origem |
|---|---|---|
| **Custo por conversa iniciada** | **≤ R$ 10** (ótimo) · ≤ R$ 11 (bom) · acima de R$ 13 revisar | Copa 2026 = R$ 9,27 (melhor) · Namorados = R$ 10,82 |
| CTR | ≥ 0,95% | Copa 1,31% · Namorados 0,96% · CP04 0,88% |
| CPC (link) | ≤ R$ 2,00 | Copa R$ 1,07 · Namorados R$ 2,86 |
| CPM | ≤ R$ 15 | Copa R$ 14,04 · Namorados R$ 12,82 |
| Frequência | manter 1,5–3,0 · >3 trocar criativo ou abrir raio · >4 pausar | CP04 saturou em 3,21+ · Copa resolveu expandindo raio |

**Resultado de referência = "conversa iniciada" (messaging_conversation_started_7d).** O pixel de compra do Meta quase não dispara, então conversa no zap é o melhor proxy de lead. Pra ROAS real, cruzar conversas com vendas fechadas.

**Aprendizados (comparativo CP04 × Namorados × Copa 2026):**
- Campanha **sazonal com data + criativo dedicado rende mais por real** que prospecção genérica sempre-ligada. CP04: 62 conv/R$1k · Namorados: 92 · Copa: 108.
- Expandir raio quando frequência cruzar 2,9 — Copa resolveu assim (40km → 60km em 26/jun) e os últimos 4 dias foram os mais baratos (R$7,04/conversa).
- Renovar criativo a cada ~2–3 semanas em campanha contínua.
- Relatório comparativo completo: `marketing/campanhas/relatorios/2026-07-01-comparativo-tres-campanhas.md`.

**Como puxar dados do Meta:** script `meta_ads_client.py` (em `.claude/skills/social-post-scheduler/scripts/`) puxa insights direto da API — comando `campaigns` lista, `insights <campaign_id>` traz métricas. Conta: senhor_colchao (888195439518063).

## Google Ads (2026)

Setup completo e funcional desde 26/jun/2026. Histórico: tracking morto de maio/2026 — consertado com `whatsapp_click`.

- **CP01C** (Search, R$15/dia): ATIVO — MAXIMIZE_CONVERSIONS otimizando para `whatsapp_click`
- **CP02A** (Display RMKT, R$5/dia): ATIVO — apenas grupo `Rmkt Site 365D` ativo
- Conversão principal: `whatsapp_click` (clique no WhatsApp do site) — GA4 → Google Ads
- Aguardar 14-21 dias para dados acumularem e fazer revisão de keywords
- Auditoria completa: `marketing/campanhas/relatorios/2026-06-26-google-ads-auditoria.md`

## Campaign Manager — atendimento WhatsApp

- 193 conversas tratadas no período Copa (15–30/jun), 313 follow-ups automáticos enviados
- Tempo médio de 1ª resposta: 4 minutos 🟢
- **Alerta crítico: 32 leads sumiram após receber o preço** — script de atendimento precisa incluir parcelamento + CTA claro no momento do preço
- Disparo "Copa 2026 — Pré-jogo" no CM falhou 100% (2.103 msgs, 0 entregues) — verificar limite de disparos em massa antes de novo broadcast

## Próximas campanhas sugeridas

| Campanha | Janela | Prioridade |
|---|---|---|
| Liquidação Inverno | Jul/2026 | Alta — estoque de inverno |
| Dia dos Pais | Ago/2026 | Alta — modelo sazonal comprovado |
| Black Friday | Nov/2026 | Planejar com antecedência |

## Candidata a skill

Rotina diária de gestão financeira: verificar boletos de fornecedores e contas pessoais a vencer, checar antecipação de cartões de crédito e saldo disponível em contas para honrar compromissos. Rodar `/mapear-rotinas` para transformar isso em skill.
