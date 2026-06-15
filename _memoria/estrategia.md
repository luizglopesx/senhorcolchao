# Estratégia

## Fase

Operação estabilizada — caixa controlado, equipe formada. Momento de atacar vendas para girar estoque alto.

## Prioridade principal

**Aumentar vendas para reduzir estoque.** Estoque cheio, fluxo de caixa ok, mas vendas abaixo do esperado. Qualquer ação deve ter como critério: vai ajudar a vender mais rápido?

## O que pode esperar

- Expansão de equipe
- Novos produtos / categorias
- Reformas estruturais

## Contexto com prazo

- Ações imediatas: promoções e campanhas para girar estoque (sem prazo fixo — até o estoque normalizar)

## Campanhas ativas (2026)

- **Dia dos Namorados 2026** — peças, posts e stories produzidos em `marketing/campanhas/dia-dos-namorados-2026/`; workflows de postagem no Instagram criados em `.github/workflows/`
- **Bota Fora Maio 2026** — campanha em `marketing/campanhas/bota-fora-maio-2026/`
- **Copa 2026** — workflows de postagem criados em `.github/workflows/` (feed + story)

## Frentes em andamento

- **Redesign de páginas de produto no Simplo 7** — layout HTML padronizado definido e aprovado. Páginas organizadas por produto em `saidas/produtos/<produto>/`. Primeiro produto (**Livorno**) finalizado: mockup com fotos fotorrealistas (hero/colchão/base) em `saidas/produtos/livorno/mockup-livorno.html`, código pronto pra colar no Simplo 7 em `descricao-simplo7.html` e imagens otimizadas em `web/`. Pendente: hospedar as imagens no Simplo 7 e colar o código no catálogo

## Benchmarks de mídia paga — Meta Ads

Referências pra avaliar campanhas novas (objetivo engajamento → conversa no WhatsApp/Messenger). Atualizar conforme novas campanhas rodarem.

| Métrica | Meta / referência | Origem |
|---|---|---|
| **Custo por conversa iniciada** | **≤ R$ 11** (bom) · acima de R$ 15 revisar | Namorados 2026 = R$ 10,82 |
| CTR | ≥ 0,95% | Namorados 0,96% vs CP04 0,88% |
| CPC (link) | ≤ R$ 3,00 | Namorados R$ 2,86 |
| CPM | ≤ R$ 13 | Namorados R$ 12,82 |
| Frequência | manter 1,5–3,0 · >3 trocar criativo · >4 pausar | CP04 saturou em 3,21+ |

**Resultado de referência = "conversa iniciada" (messaging_conversation_started_7d).** O pixel de compra do Meta quase não dispara, então conversa no zap é o melhor proxy de lead. Pra ROAS real, cruzar conversas com vendas fechadas.

**Aprendizados (comparativo CP04 maio vs Dia dos Namorados jun/2026):**
- Campanha **sazonal com data + criativo dedicado rende mais por real** que prospecção genérica sempre-ligada. Mesma verba (~R$ 520): Namorados fez 50 conversas, CP04 fez 32.
- Renovar criativo a cada ~2–3 semanas em campanha contínua (a CP04 saturou rodando há muito tempo).
- Priorizar próximas datas: **Dia dos Pais (ago), Black Friday (nov), Natal.**
- Relatório completo: `marketing/campanhas/relatorios/2026-06-15-comparativo-cp04-vs-namorados.md`.

**Como puxar dados do Meta:** script `meta_ads_client.py` (em `.claude/skills/social-post-scheduler/scripts/`) puxa insights direto da API — comando `campaigns` lista, `insights <campaign_id>` traz métricas. Conta: senhor_colchao (888195439518063).

## Candidata a skill

Rotina diária de gestão financeira: verificar boletos de fornecedores e contas pessoais a vencer, checar antecipação de cartões de crédito e saldo disponível em contas para honrar compromissos. Rodar `/mapear-rotinas` para transformar isso em skill.
