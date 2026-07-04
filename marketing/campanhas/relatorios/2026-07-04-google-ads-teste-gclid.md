---
tipo: auditoria-campanhas
data_analise: 2026-07-04
fonte: Google Ads API v21 + teste direto de servidor (curl)
canais: [google-ads]
campanhas_ativas: [CP01C, CP02A, CP02B, CP03A]
---

# Teste do gclid — 04/07/2026

## Contexto

Confirmação do "próximo passo" deixado pendente na auditoria de 03/07: reconfirmar se o `gclid` chega intacto na landing page depois da correção de Final URL (www → sem-www) aplicada nos 9 anúncios da CP01C e CP02A.

## Resultado do teste

**Domínio correto, sem www (`senhorcolchao.com.br`) — CONFIRMADO OK.**

Requisição direta simulando clique de anúncio:
```
https://senhorcolchao.com.br/?utm_source=teste&gclid=TESTE123456
→ HTTP 200 direto (sem redirect), query string preservada
```

A página carrega corretamente as duas tags:
- GA4: `G-BMP4LRZ1L5`
- Google Ads: `AW-11369026602`

Consulta à API confirmou os 9 anúncios corrigidos em 03/07 (CP01C: Branding, Colchões De Espuma, Cama Box Espuma, Colchões de Molas, Cama Box Molas; CP02A: Rmkt Site 540D x2, Rmkt Site 365D x2) estão `ENABLED` + `APPROVED` — a revisão de política já liberou, sem ficar travado em `REVIEW_IN_PROGRESS`.

**Confirmado com www (`www.senhorcolchao.com.br`) — problema de origem continua ativo.**
```
https://www.senhorcolchao.com.br/?...&gclid=...
→ 301 redirect para https://senhorcolchao.com.br/, query string descartada
```
Isso não afeta mais os anúncios (Final URL já corrigida pra sem-www), mas qualquer link externo com www ainda perde o gclid/utm (e-mail, QR code, etc. — ver ação pendente com hospedagem/DNS).

## Confirmação com clique real (usuário, fora da ferramenta de diagnóstico)

Busca real no Google por "colchoes em barretos" (feita de São Joaquim da Barra, dentro do raio de segmentação `PRESENCE_OR_INTEREST`), clique no anúncio "SR. COLCHÃO SLEEP STORE" (grupo Branding). URL de destino chegou:

```
https://senhorcolchao.com.br/?utm_source=google&utm_medium=cpc&utm_campaign=21478508604
  &utm_content=706566484730&utm_term=colch%C3%B5es%20em%20barretos
  &gad_source=1&gad_campaignid=21478508604&gbraid=0AAAAAqWllCrHs4nooWT5M49CsqK4bcdYY
  &gclid=EAIaIQobChMImp-Fl4K5lQMV1kFIAB0r8RjFEAAYASAAEgLANvD_BwE
```

Confere em tudo com o teste sintético acima:
- `utm_content=706566484730` é exatamente o ID do anúncio do grupo **Branding** (CP01C) confirmado via API como `ENABLED`/`APPROVED`
- Domínio de destino: `senhorcolchao.com.br` (sem www) — correto
- `gclid`, `gad_source`, `gad_campaignid`, `gbraid` e todos os UTMs chegaram intactos

**Isso fecha o teste do gclid com prova real, não só simulação via curl.**

## Confirmação da atribuição no GA4 (fecha a dúvida aberta desde 02/07)

Checagem no GA4 → Tempo real → card "Origem atribuída ao primeiro usuário" mostrou `(direct)` — mas essa dimensão é fixa no primeiro contato do dispositivo com o GA4, não reflete a sessão atual (o teste foi feito em navegador anônimo, então isso é menos esperado, mas essa dimensão de qualquer forma não é a certa pra validar sessão isolada).

Checagem correta, no relatório padrão **Aquisição → Aquisição de tráfego** (dimensão "Sessão de origem/mídia", agrupada por "Grupo principal de canais"), período de hoje (04/07):

| Canal | Sessões |
|---|---|
| Unassigned | 3 (75%) |
| Cross-network | 2 |
| **Paid Search** | **1** |

O clique de teste (único clique pago feito hoje) foi corretamente classificado como **Paid Search**. Isso confirma que a atribuição de sessão está funcionando corretamente pro tráfego pago — não é mais suspeita, é confirmado com dado real de hoje.

**Nota separada, não bloqueante:** "Unassigned" continua sendo a maior fatia (75% hoje, mesmo padrão do achado de 02/07 com o `whatsapp_click`). É um problema diferente do gclid — não afeta a conclusão desse teste, mas continua em aberto pra investigação futura (possivelmente tráfego direto real, sem relação com o Ads).

**Achado técnico à parte, encontrado no código-fonte da página — CORRIGIDO (2026-07-04):** o gtag estava instalado **duas vezes** na mesma página (`https://senhorcolchao.com.br/`). Origem confirmada: a integração nativa **Integrações → Google Analytics** do Simplo7 já injeta um bloco cobrindo `G-BMP4LRZ1L5` (GA4) e `AW-11369026602` (Ads); havia um segundo bloco colado manualmente em **Aparência → Scripts → Cabeçalho (Header)**, repetindo só o `G-BMP4LRZ1L5` (comentário antigo `<!-- Google tag (gtag.js) -->`). Usuário removeu o bloco manual, mantendo google-site-verification, facebook-domain-verification e Hotjar (que também estavam nesse campo). Confirmado via curl pós-alteração: só sobrou 1 `<script src=".../gtag/js">` e os 2 `gtag('config', ...)` esperados (`G-BMP4LRZ1L5` e `AW-11369026602`), sem duplicação.

## Achado novo — 2 campanhas ainda apontavam pro domínio errado, com certificado SSL expirado

Consulta à API revelou 2 campanhas com anúncio `ENABLED` **fora do escopo da correção de 03/07** (que cobriu só CP01C e CP02A), ainda usando Final URL `https://www.srcolchao.com.br/...` (domínio errado — falta "enhor" — **e** com www):

- **CP02B** `[ D ] [ VENDAS / RMKT / PG AMX ONE ]` — Display Remarketing
- **CP03A** `[ YT ] [ VENDAS / RMKT / SITE ]` — YouTube Remarketing

Teste direto nesse domínio:
```
https://www.srcolchao.com.br/... → SSL certificate problem: certificate has expired
Certificado válido: 29/12/2025 a 29/03/2026 — expirado há mais de 3 meses
```

**Correção (2026-07-04): status real das campanhas checado antes de agir** — `ad_group_ad.status = ENABLED` só reflete o anúncio, não a campanha. Status real:
- **CP02B**: campanha `PAUSED` — não estava gastando verba hoje, mas problema ficaria latente pra uma reativação futura.
- **CP03A**: campanha `REMOVED` (excluída permanentemente) — nunca mais vai servir, não vale a pena editar.

Ou seja, **não havia desperdício ativo de verba** nas 2 campanhas hoje — o achado inicial superestimou a urgência.

## Ação executada (2026-07-04)

**CP02B**: Final URL do anúncio (ID `711591343866`, grupo "Ad group 1") corrigida via API de `https://www.srcolchao.com.br/cama-box-molas/queen/cama-box-queen-size-mola-ensacada-amx-one-158x198x70-p` para `https://senhorcolchao.com.br/`. O produto original (AMX One) não existe mais no domínio novo (path retorna 404) — busca no sitemap não achou substituto exato (o mais próximo, "Dakota", tem profundidade diferente: 72cm vs 70cm do original), então optou-se por apontar pra home, mesmo padrão usado nos outros 9 anúncios corrigidos em 03/07. Confirmado via API: `finalUrls` atualizado, `approvalStatus` voltou pra `UNKNOWN` (entra em revisão de política novamente, sem urgência já que a campanha está pausada).

**CP03A**: mantida sem alteração — campanha `REMOVED`, correção não teria efeito prático.

## Pendências

1. Confirmar se `srcolchao.com.br` (domínio errado) ainda é necessário pra algo, ou se pode ser abandonado — parece resíduo de uma migração de domínio antiga (era o site antes, hoje é `senhorcolchao.com.br`)
2. Reportar à hospedagem/DNS o redirect www → sem-www que descarta query strings (afeta qualquer link externo com www, não só Ads)
3. Se CP02B for reativada no futuro, decidir se cria um anúncio novo apontando pro produto certo (perguntar ao usuário qual substituiu o AMX One, se algum) em vez de manter a home

## Conclusão sobre o gclid

O problema original (redirect descartando o gclid) está **resolvido e confirmado com dado real** para as campanhas corrigidas em 03/07 — o clique de teste apareceu como sessão "Paid Search" no GA4. Pode confiar no tracking dessas campanhas a partir de agora. As 2 campanhas com domínio errado + certificado expirado (CP02B, CP03A) são um problema novo e mais grave (perda total do clique, não só do parâmetro), e o gtag duplicado é um item de limpeza técnica — nenhum dos dois invalida a conclusão principal.
