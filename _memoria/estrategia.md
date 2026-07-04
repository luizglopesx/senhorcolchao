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

- **Durma como Campeão** (planejada, ainda não lançada) — 2 fases: Copa Mata-Mata (07–19/07, tema "a gente tá na mata-mata dos preços também") e Férias (20–31/07, com pivô automático se o Brasil cair antes). Meta de receita julho: R$200k (ideal R$215k). Produto prioritário: conjunto Colchão+Box+Cabeceira. Planejamento e artes em `marketing/campanhas/julho-2026-durma-como-campeao/`

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

- **CP01C** (Search, R$25/dia desde 03/07 — antes R$15/dia estourava quase todo dia): ATIVO — MAXIMIZE_CONVERSIONS otimizando para categoria **Contato** (whatsapp_click + clique-pra-ligar + ligação). Compra/Carrinho/Checkout existem como conversão mas são **não-biddable** nessa campanha de propósito — protege o lance de ser diluído por carrinho (mais fácil de disparar que WhatsApp real)
- **CP02A** (Display RMKT, R$5/dia): **PAUSADA manualmente em 03/07** (antes ativa com grupos Rmkt Site 540D e Rmkt Site 365D ambos habilitados)
- Conversão principal pra CPL: `whatsapp_click` — coluna "Conversões" só conta Contato; "Todas as conv." inclui carrinho/compra e não deve ser usada pro cálculo de CPL
- **Achado crítico 03/07: causa raiz de ~90 dias de zero conversão foi encontrada e corrigida.** O site tinha um redirect www→sem-www que descartava a query string inteira (gclid, utm, tudo) antes da página carregar. Corrigido: 9 anúncios + 25 sitelinks/promoção migrados pra URL sem www. Metas de conversão Compra/Carrinho/Checkout também estavam com "Configuração incorreta" — corrigido.
- **Confirmado em 04/07, com dado real: o gclid chega intacto e a atribuição funciona.** Clique real de teste (busca "colchoes em barretos") apareceu classificado como sessão **"Paid Search"** no GA4 (Aquisição de tráfego) — fecha em definitivo a dúvida que estava em aberto desde 02/07. Detalhe: `www.senhorcolchao.com.br` (com www) ainda descarta a query string — não afeta mais os anúncios, mas afeta qualquer link externo com www (e-mail, QR code). **Pedido de correção do redirect já enviado à hospedagem (OpsEmpresas)** — domínio está no registro.br, mas quem controla o servidor/redirect é a OpsEmpresas. Resposta pendente.
- **Achado 04/07: CP02B e CP03A ficaram de fora da correção de 03/07**, ainda apontando pro domínio errado `www.srcolchao.com.br` (SSL expirado desde 29/03). Checado o status real antes de agir: CP02B estava `PAUSED` (não gastava verba) — Final URL corrigida pra `senhorcolchao.com.br`. CP03A estava `REMOVED` (excluída, nunca mais serve) — não mexida.
- **Achado 04/07: gtag duplicado no Simplo7, corrigido.** Integração nativa (Integrações → Google Analytics) já cobria GA4 + Ads; havia um bloco redundante colado manualmente em Aparência → Scripts → Cabeçalho, repetindo só o GA4. Usuário removeu o bloco manual — confirmado sem duplicação.
- **Relógio de "aguardar dados acumularem" reinicia em 03/07** (não em 26/06) — antes da correção, nenhum clique pago carregava atribuição corretamente, então dado anterior a essa data não serve pra calcular CPL
- Decisão pendente: calcular CPL real do Google Ads (custo ÷ Conversões) depois de 2-4 semanas de dado limpo, e comparar com CPL do Meta Ads pra decidir alocação de verba entre os dois canais
- Auditorias: `marketing/campanhas/relatorios/2026-06-26-google-ads-auditoria.md` → `2026-07-02-google-ads-auditoria.md` → `2026-07-03-google-ads-auditoria.md` → **`2026-07-04-google-ads-teste-gclid.md`** (mais recente, com a confirmação final do gclid)

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
