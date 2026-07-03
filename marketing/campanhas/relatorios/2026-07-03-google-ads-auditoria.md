---
tipo: auditoria-campanhas
data_analise: 2026-07-03
fonte: Google Ads API v21
canais: [google-ads]
campanhas_ativas: [CP01C, CP02A]
---

# Auditoria Google Ads — 03/07/2026

## Contexto

Follow-up direto da auditoria de 02/07. Motivo: teste de gclid em Barretos (ferramenta de Diagnóstico e visualização de anúncios) mostrou "anúncio não sendo exibido" mesmo com keyword batendo. Investigação via API confirmou orçamento estourado no momento do teste, e abriu pra uma auditoria maior de keywords, negativas e setup de conversão pra viabilizar cálculo de CPL.

---

## Achado 1 — Orçamento estourando quase todo dia (causa do teste de gclid ter falhado)

- Orçamento R$15/dia estourado em 9 de 14 dias analisados (18/06–02/07), até 2x o teto num dia (R$29,85)
- No dia do teste (03/07), a campanha já tinha gasto R$15,85 de R$15,00 **antes** do teste rodar — anúncio saiu do ar por falta de verba, não por erro de segmentação/aprovação
- Segmentação, aprovação de anúncio/keyword e domínio de destino: todos corretos (confirmado via API)

## Achado 2 — Keywords e negativas

- **Negativas**: estrutura boa. 4 listas compartilhadas (Padrão: 30, Concorrentes: 27, Grátis: 12, Cidades: 3) + 9 negativas de campanha + 6 negativas de grupo (marcas concorrentes no Branding)
- **Keywords do grupo Branding**: quase todas já migradas de broad → phrase na auditoria de 02/07. Sobrava 1 keyword ainda em broad match ativo: **"colchoes barretos"**
- **544 termos de pesquisa reais (30 dias) analisados**: zero conversões em qualquer um. Vazamento identificado — buscas genéricas ("cama box casal", "cama queen casal", "colchão solteiro") e termos de marcas de terceiros (apolo, af colchões, anjos, base sommier) caindo no grupo Branding via broad match residual

## Achado 3 — Setup de conversão quebrado, impede cálculo de CPL

- Nenhuma ação de conversão relevante (compra, whatsapp_click) está contabilizando como "Conversões" na conta
- Ação "COMPRA REALIZADA" (GA4): **removida**
- `whatsapp_click` (GA4): ativa, mas não contabilizada nas métricas de conversão
- 4 ações órfãs de "Smart Campaign" (chamada, rota no mapa) — resíduo de integração antiga, conta não roda mais Smart Campaigns
- **Resultado 30 dias**: R$463,89 (CP01C) + R$150,79 (CP02A) = R$614,68 gastos, 0 conversões em qualquer categoria, em qualquer campanha
- CPL do Google Ads **impossível de calcular hoje** — problema de medição, não necessariamente de performance real. Comparar com Meta Ads agora seria decisão baseada em dado quebrado

## Achado 4 — CAUSA RAIZ do gclid encontrada e corrigida: redirect www → sem-www derruba a query string

Teste de clique real feito pelo usuário (busca "colchao barretos" no Google, fora da ferramenta de diagnóstico, com segmentação da campanha confirmada como `PRESENCE_OR_INTEREST` — não precisa estar fisicamente em Barretos):

- Anúncio da concorrente (Castor): landing chegou com `gad_source`, `gad_campaignid`, `gbraid` **e** `gclid` intactos — prova que o Google está gerando e passando o gclid normalmente
- Anúncio da Senhor Colchão: landing chegou em `https://senhorcolchao.com.br/` **sem nenhum parâmetro**

Testado via requisição direta (sem seguir redirect automaticamente):
- `https://www.senhorcolchao.com.br/?utm_source=teste&gclid=TESTE123456` → **301 redirect para `https://senhorcolchao.com.br/`, query string completamente descartada**
- `https://senhorcolchao.com.br/?utm_source=teste&gclid=TESTE123456` → **200 direto, sem redirect, query string preservada**

**Causa raiz confirmada:** o redirect de www → sem-www no servidor do site descarta todos os parâmetros de URL (gclid, utm_source, utm_medium, etc.) antes da página carregar. Isso não tem relação com Google Ads, GA4 ou tracking template — é puramente uma configuração de redirect do lado do site (hospedagem/DNS). Afeta **100% dos cliques pagos**, não só busca — os 9 anúncios ativos da conta (Search e Display) usavam a mesma Final URL com www.

Tracking template da conta (`{lpurl}?utm_source={_source}&utm_medium={_medium}&utm_campaign={_campaign}&utm_content={_content}&utm_term={_term}`) e auto-tagging: confirmados corretos, não são a causa.

---

## Ações executadas (via API)

| Ação | Resultado |
|---|---|
| Orçamento CP01C: R$15 → R$25/dia | ✅ Aplicado |
| "colchoes barretos" migrada de BROAD → PHRASE (grupo Branding) | ✅ Aplicado — broad original removida |
| Ocultar 4 ações de conversão órfãs (Smart Campaign) | ❌ Bloqueado pela API do Google (`MUTATE_NOT_ALLOWED` — recurso gerenciado pelo Google, imutável). Não afeta o cálculo de CPL (não geram custo nem competem como meta de lance) — deixado como está |
| Final URL corrigida de `https://www.senhorcolchao.com.br/` → `https://senhorcolchao.com.br/` nos 9 anúncios ativos (CP01C: Branding, Colchões De Espuma, Cama Box Espuma, Colchões de Molas, Cama Box Molas; CP02A: Rmkt Site 540D x2, Rmkt Site 365D x2) | ✅ Aplicado |
| Mesma correção (www → sem www) em **25 assets de extensão** (sitelinks + 1 promoção) ativos na CP01C, em nível de grupo de anúncio, campanha e conta — descoberto porque sitelinks têm URL própria, independente da URL do anúncio principal | ✅ Aplicado |

## Achado 5 — Sitelinks pausados/removidos com domínio errado (srcolchao.com.br), não afeta tráfego ativo

Encontrados vários sitelinks antigos apontando pra `www.srcolchao.com.br` (domínio errado, sem "enhor") em quase todos os grupos da CP01C — mas todos com status **PAUSED** ou **REMOVED** no vínculo do grupo/campanha. Confirma o que a auditoria de 02/07 já tinha visto: domínio errado existe na conta como resíduo histórico, mas não está servindo tráfego real hoje. Não precisou de ação.

## Achado 6 — Metas de conversão "Compra", "Adicionar ao carrinho" e "Iniciar finalização de compra" com Configuração Incorreta

Print do painel (Conversões → Resumo) mostrou:
- **Compra**: Status "Configuração incorreta" — 0 ações principais (a única ação existente, `srcolchao.com.br – GA4 (web) purchase`, estava marcada como Secundária)
- **Adicionar ao carrinho** e **Iniciar finalização de compra**: mesmo problema, mesma causa
- **Contato**: já estava com status "Ativa" — `whatsapp_click` já era ação Principal (bom sinal, não precisou mexer)

**Correção aplicada via API** (diferente das ações "Smart Campaign" bloqueadas antes — essas são ações GA4 normais, editáveis): marcadas como **Principal** (`primary_for_goal = true`):
- `srcolchao.com.br – GA4 (web) purchase`
- `srcolchao.com.br – GA4 (web) begin_checkout`
- `srcolchao.com.br – GA4 (web) add_to_cart`

Confirmado via API pós-alteração: as 3 ações agora retornam `primaryForGoal: True`. Meta "Compra" deve sair de "Configuração incorreta" pra "Ativa" no painel (checar visualmente pra confirmar).

## Efeito colateral esperado das correções de URL

Alterar Final URL de anúncio ou de asset (sitelink/promoção) reabre a revisão de política do Google — os 9 anúncios e os 25 assets corrigidos hoje devem passar um tempo (minutos a poucas horas) em `REVIEW_IN_PROGRESS` antes de voltar a exibir normalmente. Se o anúncio "sumir" no teste logo após a correção, é esperado, não é um novo problema.

## Próximos passos (bloqueador para CPL)

1. **Reconfirmar o gclid** com um novo clique real após a revisão de política liberar (esperar algumas horas) — esperado: URL de destino agora deve chegar com `gclid=` intacto, seja clicando no título do anúncio ou num sitelink
2. Reportar pra quem administra a hospedagem/DNS de senhorcolchao.com.br que o redirect www → sem-www está descartando query strings — vale corrigir na raiz mesmo com o contorno já aplicado no Google Ads (qualquer link externo com www + parâmetros ainda perde os dados, ex: campanhas de e-mail, QR code, Meta Ads se algum anúncio usar www)
3. **Recriar/corrigir a ação de conversão de compra e reativar o `whatsapp_click` como meta contabilizada** — via Configurações de Conversão no painel (não disponível por API pelo visto acima)
4. Só depois de 1 e 3, com ~2-4 semanas de dado limpo: calcular CPL real do Google Ads e comparar com Meta Ads pra decisão de alocação de verba
5. Acompanhar se o orçamento novo (R$25/dia) para de estourar e se a força dos anúncios em "Colchões de Molas" e "Cama Box Molas" sai de POOR
