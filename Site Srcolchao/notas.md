# Site novo — Senhor Colchão

## Situação atual

- Site hoje: https://senhorcolchao.com.br
- Plataforma: Simplo 7
- Hospedagem: Ops Empresas (Barretos)
- Problema: plataforma engessada, limita o layout e as regras de customização

## Ideia

Criar um site novo, com layout próprio, sem ficar preso às regras/templates da Simplo 7.

## Decisões já tomadas

- **Escopo:** e-commerce completo — carrinho, pagamento online e gestão de estoque integrada. Cliente compra direto pelo site (não é só vitrine pro WhatsApp).
- **Simplo 7:** sair totalmente. Migrar pra outra stack/plataforma, sem depender mais deles (nem backend, nem front-end). ⚠️ **Em revisão em 2026-07-08** — ver seção "Descoberta: Simplo 7 = wBuy (HostGator)" abaixo, pode não ser mais necessário trocar de empresa.
- **Abordagem:** começar do zero — "migrar" aqui não significa carregar dados/histórico da Simplo 7 pra plataforma nova. É construir o site novo do zero (catálogo, estrutura, conteúdo), não transportar o que já existe lá.
- **Plataforma escolhida (recomendação, 2026-07-08): Nuvemshop Impulso (R$164/mês).** ⚠️ **Em revisão** — ver descoberta do wBuy abaixo, que pode ser opção melhor (mais barata e sem trocar de empresa). Motivos originais da escolha: só R$49 a mais que os R$115 pagos hoje; resolve o problema de layout engessado (libera código do tema); carrinho/checkout/pagamento Pix/estoque já inclusos; plataforma brasileira (sem risco cambial, suporte em português); zero manutenção de servidor. Descartadas: Shopify (cobra em dólar + taxa extra de gateway no Brasil), VTEX (enterprise, caro demais), WooCommerce/VPS própria (exige manutenção técnica contínua que não tem quem faça).
- **Quem constrói o tema (2026-07-08): sem freelancer.** Luiz + Claude Code constroem o tema juntos — Claude escreve o código (HTML/CSS/JS na estrutura Nuvemshop) e roda o Nuvemshop CLI direto no terminal do projeto pra sincronizar com a loja; Luiz entra com referências visuais, conteúdo e feedback de cada tela.

### Pré-requisitos pra começar a construção

1. Conta Nuvemshop criada com plano Impulso ativo (acesso ao código do tema)
2. Autenticação do CLI feita por Luiz (login/autorização via navegador)
3. Referências visuais (sites/lojas de inspiração, prints, ou descrição do estilo desejado)
4. Conteúdo inicial (fotos de produtos, textos, produtos de exemplo pra montar a página de produto)

**Fluxo de trabalho previsto:** definir estrutura de páginas (home, categoria, produto, carrinho) → Claude monta primeira versão de cada uma → Luiz revisa no preview ao vivo do CLI → itera.

## Perguntas em aberto (pra amadurecer)

- [x] ~~Qual plataforma/stack usar pro e-commerce novo?~~ → Nuvemshop Impulso (ver Decisões)
- [ ] Vale a pena reaproveitar fotos/textos de produtos já existentes na Simplo 7 como ponto de partida, ou tudo será refeito do zero também?
- [ ] Precisa de integração com meios de pagamento específicos (Pix, cartão, boleto)? Algum gateway preferido?
- [ ] Como fica a gestão de estoque — precisa integrar com algum sistema que já usam hoje?
- [ ] Quem vai manter o site depois de pronto? (equipe não-técnica → precisa de painel fácil de usar)
- [ ] Domínio senhorcolchao.com.br fica onde? Pode migrar de hospedagem (sair da Ops Empresas)?
- [ ] Referências de sites concorrentes/inspiração de layout?
- [ ] Prazo e orçamento (plataforma, hospedagem, ferramentas, eventual dev)?
- [ ] Precisa rodar em paralelo com o site atual durante a transição, ou pode trocar de uma vez?

## Descoberta: Simplo 7 = wBuy (HostGator) (2026-07-08)

Luiz encontrou: a Simplo 7 foi comprada pela HostGator em 2023, e a solução de e-commerce deles hoje é a **wBuy** — mesma empresa, plataforma evoluída/rebatizada. Isso reabre a pergunta: talvez não precise trocar de empresa/provedor, só de plano/plataforma dentro da própria HostGator.

### Planos wBuy

Hoje: Simplo 7 (HostGator) = **R$ 115/mês**.

| Plano wBuy | Preço mensal | Catálogo | Customização de layout |
|---|---|---|---|
| Iniciante | R$ 59 | até 200 produtos | Só temas grátis prontos, sem HTML/CSS |
| **Turbo** | **R$ 149** | até 500 produtos | **CSS adicional + editar HTML + criar tema do zero** |
| Expansão | R$ 299 | até 1.000 produtos | Idem Turbo + mais recursos |
| Elite | R$ 499 | até 5.000 produtos | Idem + recursos avançados |

**Por que isso é relevante:** o plano **wBuy Turbo (R$149/mês)** já libera edição de HTML/CSS e criação de tema do zero — mesmo nível de liberdade de layout que o Nuvemshop Impulso, só que R$15 mais barato **e dentro da mesma empresa que já hospeda a loja hoje**. Isso tende a facilitar a transição (possível upgrade de plano em vez de trocar de provedor/negociar com empresa nova, reapontar DNS, etc.).

### Como funciona a edição de tema na wBuy (confirmado 2026-07-08)

- Temas feitos em **HTML + CSS + JavaScript** usando o motor de templates **Twig** (tecnologia estabelecida, parecida com o Liquid do Shopify).
- Personalização básica: tela "Temas" → "Personalizar tema" (cores, tamanhos, fontes, preview em tempo real, sem código).
- Edição avançada: **direto no painel web** (Opções → Editar código) — diferente da Nuvemshop, que usa CLI local. Existe documentação própria de temas (doc-templates.wbuy.com.br) e uma loja de templates prontos (temas.wbuy.com.br), ecossistema parecido com o Shopify Theme Store.

### Migração Simplo 7 → wBuy (confirmado 2026-07-08)

**Não é automática** — precisa falar com um especialista da wBuy (serviço de migração dedicado, inclusive pra quem já é cliente HostGator/Simplo7). O serviço inclui:
- Mapeamento completo da loja atual (produtos, clientes, regras)
- Importação do histórico de pedidos e base de clientes (se optarem por aproveitar)
- **Planejamento de redirecionamentos 301 pra preservar o SEO** — resolve de fábrica a parte mais delicada do roteiro de migração original
- Domínio atual (senhorcolchao.com.br) pode ser mantido

**Leitura:** isso fortalece a wBuy como opção — mesma empresa que já hospeda hoje, plano mais barato que Nuvemshop Impulso (R$149 vs R$164), customização de tema real, e caminho de migração testado (mesmo que decidam não aproveitar o catálogo antigo, reduz risco da transição, principalmente no SEO).

Fontes: [Loja Virtual HostGator agora é wBuy](https://www.wbuy.com.br/hostgator), [wBuy planos e preços](https://www.wbuy.com.br/planos/), [wBuy — migrar loja](https://www.wbuy.com.br/migrar-loja/), [wBuy — documentação de templates](https://doc-templates.wbuy.com.br/)

### ⚠️ Contradição encontrada — resposta do suporte HostGator (ticket Z6JYDW-47X11, 2026-07-09)

Abriu chamado com o suporte HostGator (loja `dlojavirtual.com`) perguntando sobre migração. A resposta trata **"Loja HostGator" e "WBuy" como plataformas/times separados** — inclusive diz que pra migrar pra WBuy é preciso falar com a equipe deles à parte. Isso contradiz a suposição registrada acima (08/07) de que Simplo 7 = wBuy = mesma plataforma.

**Planos informados pela HostGator (Loja Virtual / dlojavirtual.com), pra quem já é cliente:**

| Plano | Mensal | Anual | Parcelado (12x) | Comissão sobre pedidos pagos |
|---|---|---|---|---|
| Básico | R$ 49,00 | R$ 346,92 | R$ 28,91 | 1,5% |
| Essencial | R$ 99,00 | R$ 653,40 | R$ 54,45 | 1,0% |
| Completo | R$ 199,00 | R$ 1.791,00 | R$ 149,25 | 0,5% |

Esses valores **não batem** com a tabela de planos WBuy pesquisada em 08/07 (Iniciante R$59 / Turbo R$149 / Expansão R$299 / Elite R$499, sem comissão mencionada). Indício de que são dois produtos diferentes dentro do grupo HostGator: a "Loja Virtual HostGator" (cobra comissão por venda) e a "WBuy" propriamente dita (sem comissão, mas plataforma separada, exige contato próprio).

**Pendências antes de decidir:**
- Confirmar com a WBuy (contato direto, conforme orientado) se as condições e o processo de migração são os mesmos, e se o plano recomendado (Turbo, R$149) é o comparável certo — sem comissão por venda muda bastante a conta vs. o plano "Completo" da tabela acima (R$199 + 0,5%).
- Nenhum dos planos "Loja HostGator" acima (Básico/Essencial/Completo) menciona liberação de HTML/CSS — só o plano Completo (R$199) tem chance de ser o equivalente a customização real; precisa confirmar.
- Manter a recomendação provisória de Nuvemshop Impulso em standby até esclarecer isso — decisão segue em aberto.

### Reputação — wBuy vs. Nuvemshop (levantado 2026-07-08, Reclame Aqui)

| | wBuy | Nuvemshop |
|---|---|---|
| Nota recente (6 meses) | 9,0 (amostra pequena — só 10 reclamações avaliadas) | 7,8/10 ("BOM") |
| Nota histórica (2022–2025) | **5,3/10 — "Ruim"**, 38 reclamações, só 50% resolvidas, 44,4% voltariam a negociar | 6,27 médio geral, 71,5% voltariam a negociar, 83,6% resolvidas |
| Queixa mais comum | **Qualidade do suporte** — atendentes descritos como rudes, pouco empáticos, respostas genéricas | Bloqueio de saldo em transações (retenção por suspeita de fraude — risco comum a qualquer gateway BR), problemas com serviço de "especialistas" pago à parte |

**Comparativo direto wBuy vs Nuvemshop:** Nuvemshop é a maior plataforma de e-commerce da América Latina, tem plano gratuito, +150 integrações nativas (ERPs, frete, marketing), não cobra por quantidade de produto. wBuy tem como diferencial integração nativa com Mercado Livre e Shopee, e recursos de omnichannel/fidelidade — mas sem desconto em plano anual e ecossistema/comunidade menor.

**Recomendação (2026-07-08):** apesar de custar R$15 a menos e ser da mesma empresa, a reputação de suporte da wBuy é historicamente mais fraca (5,3/10 "Ruim"), o que pesa bastante pro caso de vocês — sem time técnico próprio, a dependência do suporte da plataforma é maior. **Leve inclinação por manter Nuvemshop Impulso**, pela reputação de suporte mais consistente e ecossistema/comunidade maior (mais tutoriais, freelancers, documentação em caso de precisar de ajuda pontual). Decisão ainda não fechada — pendente de confirmação do usuário.

Fontes: [wBuy — Reclame Aqui](https://www.reclameaqui.com.br/empresa/wbuy-lojas-virtuais/), [Nuvemshop — Reclame Aqui](https://www.reclameaqui.com.br/empresa/nuvem-shop/), [WBUY ou Nuvemshop: qual a melhor plataforma](https://plataformasdeecommerce.com.br/wbuy-ou-nuvemshop-qual-a-melhor-plataforma-em-2024/)

## Hospedagem: VPS própria vs. infra de terceiros

Pergunta original: dá pra usar a VPS própria e construir um painel de admin, ou é melhor infra de terceiros?

- **Painel de admin não se constrói do zero** — isso é projeto de meses. Em infra de terceiros (Nuvemshop, Shopify, VTEX) o painel já vem pronto. Auto-hospedando, usa-se uma plataforma open-source já pronta com painel embutido (ex: WooCommerce/WordPress, Medusa.js).
- **Trade-off principal:** terceiros = sem preocupação com servidor/segurança/backup/PCI compliance, mas mensalidade + menos controle. VPS própria = controle total e sem mensalidade de plataforma, mas exige manutenção técnica contínua (hoje ninguém do time faz isso).
- **Ressalva importante (levantada por Luiz):** nem toda plataforma de terceiros resolve o problema de layout engessado — planos de entrada (ex: Nuvemshop Essencial) também são baseados em templates fechados, igual a Simplo 7.

### Comparativo de preço e liberdade de layout (levantado em 2026-07-08)

Hoje: Simplo 7 + hospedagem HostGator = **R$ 115/mês**.

| Opção | Preço mensal | Liberdade de layout |
|---|---|---|
| Simplo 7 (atual) | R$ 115 | Baixa — regras fixas da plataforma |
| Nuvemshop Essencial | R$ 69 | Média — +60 templates prontos, sem acesso ao código |
| **Nuvemshop Impulso** | **R$ 164** | **Alta — libera acesso ao código-fonte (HTML/CSS/JS)** |
| Nuvemshop Escala | R$ 449 | Alta + automações/relatórios avançados |
| Shopify Basic | ~US$29 (~R$150, câmbio variável) | Alta — tema em Liquid, muito flexível; cobra em dólar; Shopify Payments não roda igual no Brasil → taxa extra de gateway externo |
| VTEX | R$ 750–1.500+ fixo/mês + 2,5–3% por pedido | Alta, mas é solução enterprise — caro demais pro porte da loja |
| WooCommerce em VPS própria | ~R$ 30–60 (só a VPS, sem mensalidade de plataforma) | Total — é só WordPress/código, zero regra de plataforma — mas exige alguém cuidando de atualização/segurança/backup continuamente |

**Leitura:** Nuvemshop Impulso (R$164, R$49 a mais que hoje) e Shopify resolvem o problema de customização sem exigir manutenção de servidor. WooCommerce em VPS dá liberdade total mas cobra isso em manutenção técnica — que hoje não tem quem faça.

**Importante — esclarecimento sobre o que o Impulso realmente adiciona:** carrinho, checkout, processamento de pagamento (Nuvem Pago) e controle de estoque já vêm em **todo plano da Nuvemshop, inclusive o gratuito (Começo)** — isso é a base da plataforma, não um diferencial pago. O que o plano Impulso (R$164) libera em cima disso é: acesso ao código-fonte do tema (HTML/CSS/JS) pra customização real de layout, mais opções de gateway de pagamento, ações em massa, taxas de pagamento menores por transação e estatísticas mais avançadas. Ou seja: o motivo de considerar o Impulso é liberdade de layout + recursos operacionais — não porque os planos mais baratos "não têm" carrinho/pagamento/estoque.

Fontes: [Nuvemshop planos e preços](https://www.nuvemshop.com.br/planos-e-precos), [Shopify pricing](https://www.shopify.com/pricing), [VTEX pricing](https://www.tec4udigital.com/post/custo-vtex-2026), [Hospedagem WooCommerce Brasil 2026](https://www.melhoreshospedagem.com/hospedagem-woocommerce/)

### Como funciona customizar tema na prática (Nuvemshop / Shopify)

Modelo dos dois: **editor visual pro dia a dia + código pra fugir do padrão**.

**Nuvemshop**
- Editor visual (arrastar/soltar) já no plano Essencial — troca cor, banner, texto, ordem de blocos sem código.
- A partir do plano Impulso: acesso aos arquivos do tema via **Nuvemshop CLI** (ferramenta de linha de comando, fluxo parecido com Git — baixa os arquivos, edita local, sincroniza de volta). Exige saber HTML/CSS/JS.

**Shopify**
- Editor visual (Theme Editor) — monta a página com "seções" e "blocos" prontos, cada um com painel de configuração.
- Código de verdade é em **Liquid** (linguagem de template própria do Shopify, parecida com HTML + tags de template) + CSS/JS/JSON. Arquitetura "Online Store 2.0" permite tornar qualquer seção editável no painel visual.
- Tem CLI própria (`shopify theme dev`) e, num nível avançado, opção "headless" (Hydrogen/Next.js) pra construir o front-end 100% do zero usando o Shopify só como motor de carrinho/pagamento por trás.

**O que é "headless" (Shopify), em detalhe:** em vez de usar o sistema de temas do Shopify (Liquid), descarta-se ele completamente e constrói-se o site como uma aplicação separada (Next.js ou Hydrogen — framework próprio do Shopify), sem nenhuma amarra de template. Esse front-end só conversa com o Shopify via API pra buscar produtos e processar carrinho/estoque — o Shopify vira puramente o motor por trás das cortinas. Vantagem: liberdade de design 100% total. Desvantagens: (1) exige dev de verdade construindo uma aplicação, não freelancer ajustando tema; (2) precisa hospedar esse front-end separadamente (custo extra); (3) manutenção contínua de código próprio; (4) checkout final normalmente continua sendo a página hospedada pelo Shopify, a menos que se pague o plano Shopify Plus (bem mais caro) pra customizar isso também. **Avaliação: provavelmente over-engineering pro porte da loja — o caminho com tema Liquid customizado já dá liberdade de design suficiente com esforço bem menor.**

**Implicação prática:** pra ter o layout "sem regras" que motivou a ideia, precisa de alguém com conhecimento técnico (freelancer/dev) pra construir a base do tema customizado uma vez. Depois de pronto, o dia a dia (trocar banner, produto, texto) fica no editor visual — o time não-técnico consegue manter sozinho. Ou seja: liberdade de design real, mas com investimento técnico pontual (não contínuo como numa VPS própria).

Fontes: [Nuvemshop CLI](https://dev.nuvemshop.com.br/en/docs/developer-tools/cli/overview), [Nuvemshop — editar código do layout](https://atendimento.nuvemshop.com.br/pt_BR/personalizacao-avancada-do-layout/como-editar-o-codigo-do-layout-da-minha-loja), [Shopify — Liquid template language](https://shopify.github.io/liquid/), [Shopify — editing theme code](https://help.shopify.com/en/manual/online-store/themes/customizing-themes/edit-code/edit-theme-code)

## Roteiro de migração

1. **Levantamento e escolha da plataforma** — decidir a stack nova (Nuvemshop, VTEX, Shopify, WooCommerce, ou algo customizado). Essa escolha muda todo o resto do processo.
2. **Montar o site do zero** — novo catálogo de produtos (fotos, descrições, preços, variações, categorias) e estoque cadastrados direto na plataforma nova. Não é importar histórico da Simplo 7 — é recriar do zero, já no layout/estrutura nova.
3. **Domínio e hospedagem** — tirar o senhorcolchao.com.br da Ops Empresas e apontar o DNS pra nova hospedagem. Dá pra fazer sem o site sair do ar, mas precisa de janela de baixo tráfego.
4. **Pagamentos** — configurar gateway novo (Pix, cartão, boleto); cada plataforma tem parceiros homologados próprios.
5. **SEO (parte mais delicada)** — se as URLs dos produtos mudarem, configurar redirecionamentos 301 (URL antiga → nova) pra não perder o posicionamento no Google. Sem isso o tráfego orgânico despenca.
6. **Reconectar integrações de marketing** — reinstalar o Pixel da Meta / Conversions API e a tag de conversão do Google Ads no site novo (já rodam campanhas nessas duas plataformas hoje — ver `.env` GOOGLE_ADS_* / meta_ads_client.py).
7. **Layout novo** — a parte que motivou a troca; aqui sim, liberdade total sem as regras da Simplo 7.
8. **Testes antes do go-live** — fluxo completo de compra (Pix, cartão, boleto), emails de confirmação, cálculo de frete.
9. **Treinar quem vai manter o site** — cadastro de produto, alteração de preço, baixa de estoque, pra não depender de uma única pessoa.
10. **Corte e monitoramento** — decidir se roda em paralelo por um tempo ou troca de uma vez; acompanhar de perto os primeiros dias (erros, links quebrados, quedas de conversão).

## Próximos passos

- Levantar o que funciona e o que não funciona no site atual (usabilidade, velocidade, conversão)
- Comparar plataformas de e-commerce candidatas (prós/contras, custo, flexibilidade de layout)
- Definir o catálogo inicial do site novo (quais produtos entram primeiro, o que fica pra depois)
- Definir cronograma de transição

---
*Pasta criada em 2026-07-08 para reunir as conversas e decisões sobre o site novo.*
