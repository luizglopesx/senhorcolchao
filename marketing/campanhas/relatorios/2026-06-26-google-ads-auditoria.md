---
tipo: auditoria-campanhas
data_analise: 2026-06-26
fonte: Google Ads API v21
canais: [google-ads]
campanhas_ativas: [CP01C, CP02A]
---

# Auditoria Google Ads — 26/06/2026

## Contexto

Primeira auditoria completa após aprovação do Acesso Básico (25/06). Tracking de conversão estava morto desde maio/2026 — consertado hoje com criação do evento `whatsapp_click`.

---

## Campanhas ativas

| Campanha | Tipo | Orçamento/dia | Gasto 30d | Cliques | Conv |
|---|---|---|---|---|---|
| CP01C — Pesquisa | Search | R$15 | R$444 | 318 | 0 |
| CP02A — Display RMKT | Display | R$5 | R$152 | 167 | 0 |

**Pausadas:** CP04A e CP04B (PMax), 001.01 (Search antiga) — sem gasto.

---

## Diagnóstico — CP01C (Search)

### Estrutura de grupos
- Branding
- Cama Box Espuma
- Cama Box Molas
- Colchões De Espuma
- Colchões de Molas

### Problema principal: quase 100% broad match
A campanha foi montada com broad match em praticamente todos os termos. O Google usou isso pra exibir anúncios em buscas que fogem do negócio local.

### Maiores gastadores (all-time)
| Palavra-chave | Gasto | Cliques | Conv |
|---|---|---|---|
| `[BROAD] casa de colchão` | R$591 | 255 | 0 🔴 |
| `[BROAD] Comprar colchão de espuma` | R$548 | 200 | 27 (histórico pré-maio) |
| `[BROAD] Loja de Colchão perto de mim` | R$489 | 208 | 0 🔴 |
| `[BROAD] Colchão de espuma preço` | R$124 | 37 | 0 |
| `[BROAD] sr colchões barretos` | R$83 | 32 | 1 |
| `[BROAD] Cama Box Molas Promoção` | R$96 | 31 | 0 |

### Termos reais que chegaram (30d)
Bons: "loja de colchão em barretos", "sr colchão barretos", "colchão casal molas ensacadas d33", "box solteiro 78x188"
Problemáticos: "meucolchao com br", "ortobom barretos", "af colchoes" (concorrentes via broad match)

---

## Diagnóstico — CP02A (Display Remarketing)

| Grupo | Público | Gasto 30d | Cliques | CTR |
|---|---|---|---|---|
| Rmkt Site 365D | Visitantes 365 dias | R$29,79 | 49 | 2,3% |
| Rmkt Site 540D | Visitantes 540 dias | R$122,63 | 118 | 2,1% |

CTR 2,3% é bom para Display. CPC R$0,91 barato. Mas 540 dias (18 meses) é período longo demais para colchão.

---

## Ações executadas hoje (26/06)

### GA4 + Google Ads — tracking
- `whatsapp_click` criado no GA4 como evento-chave (`click` + `link_url contém wa.me`)
- Cliques de saída confirmados ativos no fluxo Enhanced Measurement
- `whatsapp_click` importado no Google Ads como conversão **Principal**, categoria Contato, origem GA4
- Smart Bidding passa a ter sinal real pela primeira vez

### CP01C — Search
- `[BROAD] casa dos colchoes` → `[EXACT] casa dos colchões` (interceptação de concorrente cirúrgica)
- `[BROAD] casa de colchão` → **PAUSADO** (R$591 gastos lifetime, 0 conversões, nome de concorrente)

### CP02A — Display
- Grupo `Rmkt Site 540D` → **PAUSADO** (18 meses é longo demais para colchão)
- Grupo `Rmkt Site 365D` → mantido ATIVO

---

## Ações complementares (27/06)

### Pagamento
- Forma de pagamento exigida corrigida pelo usuário — campanhas sem interrupção.

### Conversões nível de campanha (crítico)
- Detectado que CP01C e CP02A tinham `PURCHASE/WEBSITE` como biddable no nível de campanha, sobrescrevendo a configuração de conta.
- Corrigido via API: `PURCHASE/WEBSITE` → não biddable | `CONTACT/WEBSITE` → biddable nas duas campanhas.
- Smart Bidding agora otimiza oficialmente para `whatsapp_click` em ambas as campanhas.

### Conversões de site — nível de conta
- `funil_de_vendas` rebaixado de Principal para Secundária pelo usuário.
- Setup final: único Principal de site = `whatsapp_click`. Ligações e direções (Google Hosted) mantidas como Principal.

### Verificação de domínio
- Anúncios enviam tráfego para `senhorcolchao.com.br`.
- GA4 stream configurado com label `srcolchao.com.br` (rótulo incorreto, não afeta coleta).
- Confirmado: GA4 tag instalada e funcionando em `senhorcolchao.com.br` — `whatsapp_click` disparou no teste.
- Cadeia completa validada: Anúncio → senhorcolchao.com.br → clique WhatsApp → GA4 → Google Ads ✅

## Próximos passos

**Aguardar 14-21 dias** para `whatsapp_click` acumular dados nas campanhas ativas.

Depois revisar:
1. Quais grupos/palavras-chave geraram cliques no WhatsApp
2. Converter broad match dos termos que convertem para phrase/exact
3. Pausar termos com foco em e-commerce ("frete grátis", "comprar online", "loja virtual") — inadequados para loja física local
4. Avaliar se `casa dos colchões` [EXACT] converte como intercepção de concorrente
5. Considerar reativar `Rmkt Site 540D` com duração reduzida (180 dias)
