---
tipo: lista-reposicao
data: 2026-07-11
periodo_base: 2026-07-01 a 2026-07-10
fonte: Bling (produtos + estoque + pedidos de venda)
meta_faturamento_mes: 200000
---

# Lista de reposição — top 10 vendas de julho

> Base: os 10 produtos que mais faturaram entre 01 e 10/07 (R$ 41.009 no total, mais da metade do faturamento do mês até agora). Todos com estoque crítico — 1 a 3 unidades.

| # | Produto | Código | Vendido (mês) | Estoque hoje | Faturado (mês) | Sugestão de compra | Comprado (12/07) | Recebido no estoque? |
|---|---|---|---|---|---|---|---|---|
| 1 | Colchão Queen Molas Ensacadas Dakota Malha 158x198x32 PT | 84800 | 2 un | 1 | R$ 8.340 | 2 | ✅ 2 | ⏳ Não |
| 2 | Colchão Espuma Queen D45 Black & White Air Double Face 27 158x198 | 92968 | 2 un | 3 | R$ 5.480 | 1 | ✅ 2 | ⏳ Não |
| 3 | Colchão Espuma Casal D33 Ícaro Black B5 138x188x20 | 100215 | 4 un | 1 🔴 | R$ 4.860 | 3 | ✅ 7 | ⏳ Não (caiu pra 1, mais 1 venda) |
| 4 | Colchão King Molas Ensacadas Dakota Malha 193x203x32 PT | 84799 | 1 un | 3 | R$ 4.800 | 1 | ✅ 1 | ⏳ Não |
| 5 | Colchão Espuma Solteiro D33 Ícaro Black B5 88x188x20 | 100217 | 6 un | 3 | R$ 4.800 | 4 | ✅ 10 | ⏳ Não |
| 6 | Colchão Solteiro Mola Ensacada Dreamer Smart B5 88x188x25 TF | 101078 | 3 un | 2 | R$ 2.859 | 2 | ✅ 6 | ⏳ Não |
| 7 | Colchão D80 Vision 158x198x28 Pillow Top | 110715 | 1 un | 2 | R$ 2.600 | ~~1~~ **0** | não precisa | — |
| 8 | Colchão Casal Mola Maxspring Tower 1380x1880x330 Bordado Double Side | 5008543 | 1 un | 3 | R$ 2.500 | ~~1~~ **0** | não precisa | — |
| 9 | Colchão Viúva Mola Maxspring Livorno 960x2030x270mm S.Pillow | 5014076 | 2 un | 2 | R$ 2.490 | ~~1~~ **0** | não precisa | — |
| 10 | Box Suede Preto 88x188x28 | 10458 | 6 un | 1 🔴 | R$ 2.280 | 6 | ✅ 6 | ⏳ Não |

**Total sugerido de reposição: 22 unidades** entre os 10 itens. **Comprado em 12/07: 34 unidades** entre 7 dos 10 itens (acima do sugerido em quase todos).

### Correção (12/07): itens 7, 8 e 9 não precisavam de compra

A fórmula original (`vendido + 1 margem − estoque`, mínimo 1) tinha um piso de 1 unidade mesmo quando o estoque já cobria a demanda do mês. Revisando com o estoque real:
- **D80 Vision**: vendeu 1, tem 2 em estoque — cobre 2x a demanda
- **Maxspring Tower**: vendeu 1, tem 3 em estoque — cobre 3x a demanda
- **Viúva Livorno**: vendeu 2, tem 2 em estoque — cobre exatamente a demanda, sem sobra mas sem furo

Nenhum dos três precisava entrar na compra de 12/07. O usuário identificou corretamente que a recomendação estava errada nesses casos.

## Prazo de entrega: ~15 dias

Compra feita em 12/07 passa pelo representante → fabricação → entrega, com prazo médio de **15 dias**. Por isso o estoque no Bling ainda não mudou (conferido em 12/07) — é esperado, não é atraso de lançamento. Previsão de chegada: **por volta de 27/07**. Até lá, o sistema/relatórios continuam mostrando o estoque crítico de antes da compra — normal, não precisa lançar nada manualmente enquanto a mercadoria não chegar de fato.

**Ponto de atenção real:** com ~15 dias de prazo, o giro dos itens de estoque baixo (Ícaro Black Casal caiu pra 1 unidade, Box Suede Preto e Dakota Queen também em 1) precisa aguentar até por volta de 27/07 sem repor. Vale monitorar se alguma dessas zera antes da entrega chegar.

## Prioridade máxima (1 unidade em estoque)

1. **Colchão Queen Dakota Mola (84800)** — 1 unidade, R$8.340 faturados, item mais valioso da lista
2. **Box Suede Preto 88x188 (10458)** — 1 unidade, alto giro (6 unidades vendidas no mês)

## Como cheguei na sugestão de compra

`sugestão = (unidades vendidas no mês até agora) + 1 unidade de margem − estoque atual`, com mínimo de 1 unidade. É uma estimativa conservadora baseada no ritmo de venda de 10 dias — ajustar conforme prazo de entrega do fornecedor e capital disponível.

## Contexto

- Faturamento de 01–10/07: R$ 72.871,90 (10 dias corridos, 8 dias com venda — 05/07 domingo, 09/07 feriado estadual)
- Ritmo projetado pro mês: R$ 225-237 mil — acima da meta de R$200k, **se o estoque não travar as vendas**
- Estes 10 itens sozinhos respondem por mais da metade do faturamento do período — ficar sem eles no meio do mês é o maior risco pra bater a meta
