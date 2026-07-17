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

- **Durma como Campeão — Fase 1** — ATIVA desde 06/07, encerra 19/07 (R$30/dia, otimizada pra CONVERSATIONS). **Quinzena fraca:** travou em 13/07 — 4 dias seguidos sem conversa nova (13-16/07), CTR (0,57% acumulado) abaixo do benchmark (0,90-1,20%), R$295,27 investidos em 11 dias, projeção de fechar em ~R$381,77 até 19/07 (dentro do R$400 aprovado, mas sem gerar retorno proporcional). Decisão em 16/07: deixar rodar sem trocar criativo (só 3 dias restantes) e não repetir o padrão na campanha seguinte. Relatórios diários em `marketing/campanhas/relatorios/AAAA-MM-DD-durma-como-campeao-snapshot.md`.
- **Fase 2 (Férias) CANCELADA em 16/07** — substituída pela Pré-Festa do Peão (ver abaixo) antes de rodar; os R$400 aprovados e nunca usados foram realocados.
- **Pré-Festa do Peão 2026** — LANÇAMENTO 20/07, roda até 09/08 (21 dias, R$600 total / ~R$28,57 dia — verba subiu de R$400 pra R$600 em 16/07, R$200 além do que estava realocado da Fase 2). Esquenta antecipando a Festa do Peão de Barretos (evento 20-30/08) — mix geral de produto com Solteiro em destaque (motivo real da demanda de agosto, ver `empresa.md`). Planejamento completo em `marketing/campanhas/pre-festa-peao-2026/planejamento-campanha.md`. 3 peças prontas via Higgsfield (feed + story + motion) — Colchão D28 Comfortopedic Solteiro (R$479), Cama Box SmartFlex Casal (R$1.690), Colchão Orthoplus Casal (R$1.390), com produto real do catálogo Supabase. **Status em 17/07 — tudo pronto, aguardando só ativação manual do Patrocinado:**
  - ✅ Instagram orgânico agendado via GitHub Actions cron (6 posts: 20/07, 28/07, 04/08)
  - ✅ Facebook orgânico agendado via API (3 posts, mesmas datas)
  - ✅ WhatsApp Status agendado via Campaign Manager (3 posts, mesmas datas)
  - ✅ Meta Ads (Patrocinado/CTWA) **montado por completo via API, pausado**: campanha `120247929494160752`, ad set `120247929500490752` (raio 40km Barretos + interesses Rodeio/Agronegócio/Móveis/Decoração/Colchão, otimizado CONVERSATIONS), 3 anúncios de vídeo com CTA WhatsApp. Falta só revisão + ativação manual no Gerenciador de Anúncios. Fluxo documentado na memória `meta-ads-ctwa-workflow`.
  - ⚠️ 3 WhatsApp Status antigos da Fase 2 cancelada (21, 23, 25/07, com preços desatualizados) mantidos ativos por decisão do usuário em 17/07 — risco conhecido, não é esquecimento.
- **Festa do Peão 2026 (campanha dedicada ao evento)** — janela reagendada em 16/07 pra **10-31/08** (assume logo após a Pré-Festa encerrar, cobre o evento 20-30/08 + rescaldo). Verba e criativo ainda não definidos.

## Campanhas encerradas (referência)

- **Copa 2026** ✅ encerrada 30/jun — 63 conversas, R$9,27/conversa. Relatório: `marketing/campanhas/relatorios/2026-06-30-aqui-da-jogo-copa-encerramento.md`
- **Dia dos Namorados 2026** ✅ encerrada 13/jun — 50 conversas, R$10,82/conversa
- **Bota Fora Maio 2026** ✅ encerrada — campanha em `marketing/campanhas/bota-fora-maio-2026/`

## Frentes em andamento

- **Redesign de páginas de produto no Simplo 7** — layout HTML padronizado definido e aprovado (8 seções, cores da marca — ver memória `pagina-produto-simplo7`). Páginas organizadas por produto em `saidas/produtos/<categoria>/<produto>/`. Já feitos: Livorno, Livorno Solteiro, Tower, Madrid, Dakota, Lancaster, Cloud, D20 Comfortopedic (colchão + cama box), D28 Comfortopedic, Box e Box Baú (por cor). Skill dedicada `/pagina-cama-box` gera a versão cama box de um produto a partir do colchão avulso já cadastrado, puxando as fotos certas do bucket Supabase. Pendente: hospedar as imagens no Simplo 7 e colar o código no catálogo — e reavaliar prioridade conforme a decisão da frente "Site novo" abaixo.

- **Site novo — saída do Simplo 7** — decisão em andamento sobre trocar de plataforma de e-commerce (motivo: Simplo 7/HostGator não libera edição de HTML em nenhum plano, só CSS). Escolha reduzida a **wBuy** (R$149/mês, mesma empresa que já hospeda hoje, mas suporte com reputação historicamente fraca) vs **Nuvemshop Impulso** (R$164/mês, leve inclinação atual, suporte e ecossistema mais fortes). Decisão ainda não fechada. Roteiro de migração, comparativos e perguntas em aberto em `Site Srcolchao/notas.md`. **Relevante pra prioridade:** se migrar, o catálogo é reconstruído do zero na plataforma nova (não é import automático da Simplo 7) — vale pesar isso antes de investir mais tempo formatando páginas de produto no Simplo 7 atual.

- **Agente de IA via WhatsApp (consulta de estoque/Bling)** — planejamento iniciado em 15/07. Ideia: consultar estoque (depois vendas e custo) no Bling direto pelo WhatsApp, sem abrir o Claude Code. Bling ERP já tem acesso leitura via `nexus-manager.js` (Receitas Manager). Registro completo em `Agente Senhor Colchao/conversa.md`. Ainda em fase de levantamento, sem decisão de arquitetura fechada.

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

- **CP01C** (Search, R$25/dia desde 03/07 — antes R$15/dia estourava quase todo dia): ATIVO — MAXIMIZE_CONVERSIONS otimizando para categoria **Contato** (whatsapp_click + clique-pra-ligar + ligação). Compra/Carrinho/Checkout existem como conversão mas são **não-biddable** nessa campanha de propósito — protege o lance de ser diluído por carrinho (mais fácil de disparar que WhatsApp real)
- **CP02A** (Display RMKT, R$5/dia): **PAUSADA manualmente em 03/07** (antes ativa com grupos Rmkt Site 540D e Rmkt Site 365D ambos habilitados)
- Conversão principal pra CPL: `whatsapp_click` — coluna "Conversões" só conta Contato; "Todas as conv." inclui carrinho/compra e não deve ser usada pro cálculo de CPL
- **Achado crítico 03/07: causa raiz de ~90 dias de zero conversão foi encontrada e corrigida.** O site tinha um redirect www→sem-www que descartava a query string inteira (gclid, utm, tudo) antes da página carregar. Corrigido: 9 anúncios + 25 sitelinks/promoção migrados pra URL sem www. Metas de conversão Compra/Carrinho/Checkout também estavam com "Configuração incorreta" — corrigido.
- **Confirmado em 04/07, com dado real: o gclid chega intacto e a atribuição funciona.** Clique real de teste (busca "colchoes em barretos") apareceu classificado como sessão **"Paid Search"** no GA4 (Aquisição de tráfego) — fecha em definitivo a dúvida que estava em aberto desde 02/07. Detalhe: `www.senhorcolchao.com.br` (com www) ainda descarta a query string — não afeta mais os anúncios, mas afeta qualquer link externo com www (e-mail, QR code). **Pedido de correção do redirect já enviado à hospedagem (OpsEmpresas)** — domínio está no registro.br, mas quem controla o servidor/redirect é a OpsEmpresas. Resposta pendente.
- **Achado 04/07: CP02B e CP03A ficaram de fora da correção de 03/07**, ainda apontando pro domínio errado `www.srcolchao.com.br` (SSL expirado desde 29/03). Checado o status real antes de agir: CP02B estava `PAUSED` (não gastava verba) — Final URL corrigida pra `senhorcolchao.com.br`. CP03A estava `REMOVED` (excluída, nunca mais serve) — não mexida.
- **Achado 04/07: gtag duplicado no Simplo7, corrigido.** Integração nativa (Integrações → Google Analytics) já cobria GA4 + Ads; havia um bloco redundante colado manualmente em Aparência → Scripts → Cabeçalho, repetindo só o GA4. Usuário removeu o bloco manual — confirmado sem duplicação.
- **Relógio de "aguardar dados acumularem" reinicia em 03/07** (não em 26/06) — antes da correção, nenhum clique pago carregava atribuição corretamente, então dado anterior a essa data não serve pra calcular CPL
- Decisão pendente: calcular CPL real do Google Ads (custo ÷ Conversões) depois de 2-4 semanas de dado limpo, e comparar com CPL do Meta Ads pra decidir alocação de verba entre os dois canais
- **Primeira conversão real confirmada em 05/07: 1 `whatsapp_click` na CP01C**, contabilizada certinho no Google Ads — fecha o ciclo gclid→atribuição→conversão iniciado em 03-04/07. Relógio de "dado limpo" segue contando a partir de 03/07.
- **Achado 06/07: keyword "Comprar colchão de espuma" (BROAD, grupo Colchões De Espuma) consumia 52% do orçamento da CP01C (R$141,97/14 dias) com zero conversão** — mesmo padrão de vazamento já visto em 03/07 no grupo Branding. Corrigido via API: migrada pra PHRASE match. Também adicionadas "pikolin" e "vitorian" (concorrentes) à lista de negativas.
- **Correção de 06/07 confirmada funcionando (checado em 08 e 11/07):** termos de busca reais da keyword migrada agora são só sobre colchão (ex: "colchão casal espuma"), nada de vazamento tipo OLX/concorrente. Negativas "pikolin"/"vitorian" seguem bloqueando, sem reincidência.
- **Estado em 11/07: 3 conversões `whatsapp_click` acumuladas em 14 dias** (05, 06 e 09/07). Dias sem conversão nova (07, 08, 10/07) são variação normal do volume da conta, não vazamento — investigado e descartado.
- **Decisão seguindo: não criar campanha nova ainda** — volume de conversão ainda baixo pra decidir alocação de verba. CP01C segue com orçamento sobrando a maior parte dos dias.
- Auditorias: `marketing/campanhas/relatorios/2026-06-26-google-ads-auditoria.md` → ... → `2026-07-06-google-ads-auditoria.md` (primeira conversão + correção de keyword) → **`2026-07-11-google-ads-auditoria.md`** (mais recente — confirmação de keywords/negativas saudáveis)

## Campaign Manager — atendimento WhatsApp

- 193 conversas tratadas no período Copa (15–30/jun), 313 follow-ups automáticos enviados
- Tempo médio de 1ª resposta: 4 minutos 🟢
- **Alerta crítico: 32 leads sumiram após receber o preço** — script de atendimento precisa incluir parcelamento + CTA claro no momento do preço
- Disparo "Copa 2026 — Pré-jogo" no CM falhou 100% (2.103 msgs, 0 entregues) — verificar limite de disparos em massa antes de novo broadcast

## Próximas campanhas sugeridas

| Campanha | Janela | Prioridade |
|---|---|---|
| Pré-Festa do Peão (esquenta) | 20/07-09/08/2026 | **Em andamento** — ver campanha ativa acima |
| **Festa do Peão de Barretos** (campanha dedicada, 10-31/08 — evento em 20-30/08) | Ago/2026 | **Alta — motor real da demanda de Solteiro em agosto** (dados de 2025: 64% da venda de Solteiro do mês concentrada nessa janela; não é o Dia dos Pais). Verba e criativo ainda a definir. |
| Black Friday | Nov/2026 | Planejar com antecedência |

## Candidata a skill

Rotina diária de gestão financeira: verificar boletos de fornecedores e contas pessoais a vencer, checar antecipação de cartões de crédito e saldo disponível em contas para honrar compromissos. Rodar `/mapear-rotinas` para transformar isso em skill.
