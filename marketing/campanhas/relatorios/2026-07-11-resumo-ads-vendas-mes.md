---
tipo: resumo-mensal
data_analise: 2026-07-11
periodo_analisado: 2026-07-01 a 2026-07-11
fonte: [Meta Ads API, Google Ads API v21, Bling]
investimento_ads_total: 396.13
faturamento_periodo: 72871.90
meta_faturamento_mes: 200000
canais: [meta-ads, google-ads, bling]
---

# Resumo do mês — Ads x Vendas (01 a 11/07/2026)

## Investimento em mídia paga

| Canal | Gasto | Resultado |
|---|---|---|
| Meta Ads (Durma como Campeão) | R$ 141,06 | 6 conversas iniciadas no WhatsApp |
| Google Ads (CP01C) | R$ 255,07 | 3 conversões (whatsapp_click) |
| **Total ads** | **R$ 396,13** | **9 contatos gerados** |

## Vendas no mesmo período (Bling)

- R$ 72.871,90 faturados, 33 pedidos (ticket médio R$ 2.208)
- Projeção do mês: R$ 225-237 mil — acima da meta de R$ 200 mil, se o ritmo se mantiver

## Leitura

- **Investimento em ads é ínfimo perto do faturamento**: R$396 representam 0,54% da receita do período. Mesmo que só uma fração dos 9 contatos gerados tenha virado venda, o retorno já compensa várias vezes o investido.
- **Não há atribuição direta hoje** — não existe rastreamento (UTM/etiqueta) ligando a conversa do WhatsApp gerada por anúncio ao pedido fechado no Bling. A conclusão possível é de **escala** (ads custam pouco perto do resultado da loja), não de causa-efeito direta por venda.
- **O gargalo do mês não é tráfego/anúncio — é estoque.** Os produtos mais vendidos estão com 1-3 unidades (ver `saidas/reposicao-estoque/2026-07-11-lista-reposicao-top-vendas.md`). Resolver isso é mais crítico pra bater os R$200k do que otimizar ainda mais os R$396 de ads.

## Próximos passos — decidido nesta conversa

Vamos implementar rastreamento de origem pra saber de verdade quais vendas vêm de qual canal:

1. **Parâmetro UTM nos anúncios** que geram clique pro WhatsApp (Meta e Google) — permite identificar de onde veio o clique antes da conversa começar
2. **Pergunta "como conheceu a loja"** registrada no início do atendimento (Campaign Manager) ou no fechamento da venda (Bling) — cria o vínculo entre conversa/pedido e canal de origem
3. Com isso, os próximos resumos mensais podem trazer CPL e ROAS reais por canal, em vez de só correlação de escala

**Status:** planejado, ainda não implementado. Retomar quando o usuário priorizar.
