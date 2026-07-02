---
tipo: auditoria-campanhas
data_analise: 2026-07-02
fonte: Google Ads API v21 + GA4
canais: [google-ads]
campanhas_ativas: [CP01C, CP02A]
---

# Auditoria Google Ads — 02/07/2026

## Contexto

Follow-up da auditoria de 26/06. Motivo: conta com 0 conversões registradas em 90 dias (todas as ações, todas as campanhas), mesmo após o conserto do `whatsapp_click` no dia 26/06. Investigação levou a mudanças reais na CP01C (Search) e CP02A (Display Remarketing).

---

## Parte 1 — Investigação do zero conversões

### GA4 confirma que o evento existe
`whatsapp_click` disparou 5 vezes / 3 usuários nos últimos 28 dias (verificado no GA4 pelo usuário). A tag funciona.

### O gap está na atribuição, não no tracking
Quebra por origem/mídia dos 5 eventos: Direct (1), Referral (1), **Unassigned (3)**, Paid Search (**0**), Paid Other (**0**). Nenhum dos cliques de WhatsApp registrados veio de tráfego pago do Google — por isso zero aparece no Google Ads, mesmo o evento existindo no GA4.

`Unassigned` representar 60% de uma amostra tão pequena (vs 1,87% no total do site) é sinal de possível problema de atribuição, mas **não foi confirmado como causa raiz** — precisa de um clique real (fora da conta, dentro da área geográfica de Barretos) checando a URL por `gclid=`. Teste tentado ficou inconclusivo (caiu numa pré-visualização de campanha pausada, sem clique real).

### Descartado como causa
- **Final URLs das campanhas ativas**: corretas, apontando pra `senhorcolchao.com.br` (o domínio errado `srcolchao.com.br` visto num teste era só da campanha CP04A, pausada — não afeta tráfego real)
- **Segmentação geográfica**: correta (Barretos, Bebedouro, Guaíra, Olímpia + raios de 10-20km)
- **Aprovação de anúncios/keywords**: 100% aprovados, sem bloqueio de política
- **Auto-tagging**: está ativado na conta

### Em aberto
Não foi possível confirmar 100% se o `gclid` está chegando corretamente do clique no anúncio até o GA4. Tracking template customizado na conta (`{lpurl}?utm_source={_source}&utm_medium={_medium}...`) é suspeito mas não comprovado como causa. **Próximo teste:** pedir pra alguém fisicamente em Barretos clicar num anúncio real (não pré-visualização) e checar se a URL final tem `gclid=`.

---

## Parte 2 — Diagnóstico e correção CP01C (Search)

### Achados
- Orçamento (R$15/dia) já estourado no dia da análise (R$17,14 gasto) — pode causar pausas intermitentes
- **Match type continua ~100% broad**, mesmo problema identificado em 26/06, nunca corrigido
- Quality Score baixo (1-5) na maioria das keywords não-branding
- Força do anúncio **POOR** em 2 dos 5 grupos (Colchões de Molas, Cama Box Molas)
- Termos de e-commerce (frete grátis, loja virtual, comprar online) continuavam ativos como keywords, inadequados pra loja física
- Relatório de termos de pesquisa real revelou desperdício: `doctor colchões` (R$12,68, clique mais caro do período), `colchão kenko light` (R$6,15), `meucolchao com br` (R$3,33) — todas buscas de marca/site de terceiros, zero conversão

### Ações executadas
1. **9 negativas de campanha adicionadas** (phrase match): `frete grátis`, `frete gratis`, `loja virtual`, `loja online`, `comprar online`, `entrega grátis`, `meucolchao`, `doctor colchões`, `colchão kenko`
2. **14 keywords convertidas de broad → phrase match** (as que já tinham tráfego/Quality Score real): termos de marca (`Sr Colchão`, `sr colchao`) e locais (`Loja de Colchão Barretos`, `colchões em barretos`, `ortobom barretos`, etc.)
3. **RSAs reescritos nos 2 grupos com força POOR** (Colchões de Molas, Cama Box Molas):
   - Removido headline com nome de concorrente (`casa dos colchoes`) que estava indevidamente nos dois anúncios
   - Removidas promessas de "frete grátis" / "comprar online" (não batem com o modelo de negócio — loja física, fecha por WhatsApp)
   - Adicionado: CTA de WhatsApp, "Entrega e Montagem Grátis" (diferencial real), menção a Barretos, prova social real (4,6★, 29 avaliações no Google)
   - Força do anúncio ficou **PENDING** logo após a edição — Google recalcula em algumas horas; checar em 03/07 se subiu de POOR

---

## Parte 3 — Diagnóstico e correção CP02A (Display Remarketing)

### Contexto da pergunta
Display Network só funciona pra loja local como **remarketing** (retocar quem já visitou o site) — nunca como prospecção fria. A CP02A já estava montada assim, corretamente.

### Achados
- **Sem limite de frequência configurado** — mesmo visitante podia ser impactado sem controle
- **~33% do gasto em mobile (R$47 de R$142 em 30 dias) caindo em apps de baixa qualidade**: Kwai, Coin Drama, Palco MP3, DramaBox Launcher, NetShort, DramaBox Lite, HD Live Wallpaper Launcher, OiTube, Vidix AI Video Generator — padrão clássico de "assista vídeo pra ganhar moeda", clique induzido/acidental
- Placements legítimos (globo.com, CNN Brasil, climatempo, correio braziliense) sem problema
- 36 categorias de apps já vinham excluídas de fábrica (proteção básica já existia)
- Grupo "Rmkt Site 540D" (18 meses) segue pausado desde 26/06 — decisão mantida

### Ações executadas
1. **Limite de frequência adicionado**: máximo 3 impressões por pessoa a cada 7 dias
2. **9 apps excluídos** como placement negativo (lista de apps de vídeo/drama/launcher acima)

---

## Resumo de mudanças aplicadas hoje

| Campanha | Ação | Qtd |
|---|---|---|
| CP01C | Negativas de campanha | 9 |
| CP01C | Keywords convertidas broad→phrase | 14 |
| CP01C | RSAs reescritos | 2 grupos |
| CP02A | Limite de frequência | 1 (3/semana) |
| CP02A | Apps excluídos | 9 |

Nenhum orçamento foi alterado. Nenhuma campanha foi pausada/ativada.

## Próximos passos

1. **Confirmar o `gclid`**: pedir clique real em Barretos (fora da conta), checar URL por `gclid=`
2. **Checar força dos anúncios em 03/07** (Colchões de Molas, Cama Box Molas) — deve sair de PENDING pra GOOD/EXCELLENT
3. **Acompanhar CTR e CPC da CP02A** depois da exclusão de apps — esperado: menos cliques totais, mas de qualidade melhor
4. Repetir a checagem de termos de pesquisa em ~15 dias pra ver se as negativas pegaram tráfego novo ruim
5. Se o `gclid` for confirmado quebrado, next: simplificar o tracking template da conta (remover `{_source}`/`{_medium}` customizados, deixar só auto-tagging)
