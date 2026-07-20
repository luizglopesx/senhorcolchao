# Auditoria — Conteúdo "01 base" que deveria ser "02 base bipartida"

Data: 2026-07-20

## Contexto

As bases do bucket Supabase `products/box-suede-<cor>/` são **bipartidas (2 módulos)** a partir do tamanho Queen (Queen, King, Super King) — confirmado visualmente nas fotos `-cena` (linha de divisão central visível na foto). Casal e Solteiro usam base única.

O campo `Conteúdo` da ficha técnica deveria refletir isso:
- Queen / King / Super King → `01 colchão + 02 base bipartida`
- Casal / Solteiro / Viúva → `01 colchão + 01 base`

Essa regra já foi registrada na skill `pagina-cama-box` (seção "Padrão de box") pra valer em páginas novas daqui pra frente.

## Precisam de correção (23 páginas)

Ainda dizem "01 colchão + 01 base" mas usam fotos `box-suede-<cor>` (bipartidas):

| Produto | Tamanho | Caminho |
|---|---|---|
| D33 Black White | Queen | `saidas/produtos/espuma/d33-black-white/queen/cama-box/descricao-simplo7-black-white-d33-queen-cama-box.html` |
| D33 Comendador | Queen | `saidas/produtos/espuma/d33-comendador/queen/cama-box/descricao-simplo7-comendador-d33-queen-cama-box.html` |
| D45 AMX | Queen | `saidas/produtos/espuma/d45-amx/queen/cama-box/descricao-simplo7-amx-d45-queen-cama-box.html` |
| D45 Black White | Queen | `saidas/produtos/espuma/d45-black-white/queen/cama-box/descricao-simplo7-black-white-d45-queen-cama-box.html` |
| D45 Black White | Super King | `saidas/produtos/espuma/d45-black-white/super-king/cama-box/descricao-simplo7-black-white-d45-super-king-cama-box.html` |
| D45 Supreme | Queen | `saidas/produtos/espuma/d45-supreme/queen/cama-box/descricao-simplo7-supreme-d45-queen-cama-box.html` |
| D45 Supreme | Super King | `saidas/produtos/espuma/d45-supreme/super-king/cama-box/descricao-simplo7-supreme-d45-super-king-cama-box.html` |
| AMX One | King | `saidas/produtos/molas/amx-one/king/cama-box/descricao-simplo7-amx-one-king-cama-box.html` |
| AMX One | Queen | `saidas/produtos/molas/amx-one/queen/cama-box/descricao-simplo7-amx-one-queen-cama-box.html` |
| Cloud | Queen | `saidas/produtos/molas/cloud/queen/cama-box/descricao-simplo7-cloud-queen-cama-box.html` |
| Cloud | Super King | `saidas/produtos/molas/cloud/super-king/cama-box/descricao-simplo7-cloud-super-king-cama-box.html` |
| Esmeralda | Queen | `saidas/produtos/molas/esmeralda/queen/cama-box/descricao-simplo7-esmeralda-queen-cama-box.html` |
| Esmeralda | Super King | `saidas/produtos/molas/esmeralda/super-king/cama-box/descricao-simplo7-esmeralda-super-king-cama-box.html` |
| Lancaster | Queen | `saidas/produtos/molas/lancaster/queen/cama-box/descricao-simplo7-lancaster-queen-cama-box.html` (inconsistente: o King do mesmo produto já está certo) |
| Madrid | Queen | `saidas/produtos/molas/madrid/queen/cama-box/descricao-simplo7-madrid-queen-cama-box.html` |
| Madrid | Super King | `saidas/produtos/molas/madrid/super-king/cama-box/descricao-simplo7-madrid-super-king-cama-box.html` |
| Nashville | King | `saidas/produtos/molas/nashville/king/cama-box/descricao-simplo7-nashville-king-cama-box.html` |
| Nashville | Queen | `saidas/produtos/molas/nashville/queen/cama-box/descricao-simplo7-nashville-queen-cama-box.html` |
| Tower | King | `saidas/produtos/molas/tower/king/cama-box/descricao-simplo7-tower-king-cama-box.html` |
| Tower | Queen | `saidas/produtos/molas/tower/queen/cama-box/descricao-simplo7-tower-queen-cama-box.html` |
| Vivere C1885 | King | `saidas/produtos/molas/vivere-c1885/king/cama-box/descricao-simplo7-vivere-c1885-king-cama-box.html` |
| Vivere C1885 | Queen | `saidas/produtos/molas/vivere-c1885/queen/cama-box/descricao-simplo7-vivere-c1885-queen-cama-box.html` |
| Vivere C1910 | King | `saidas/produtos/molas/vivere-c1910/king/cama-box/descricao-simplo7-vivere-c1910-king-cama-box.html` |
| Vivere C1910 | Queen | `saidas/produtos/molas/vivere-c1910/queen/cama-box/descricao-simplo7-vivere-c1910-queen-cama-box.html` |

## Já corretas — não precisam de nada (9)

- Dakota Queen — `saidas/produtos/molas/dakota/queen/cama-box/`
- Dakota Super King — `saidas/produtos/molas/dakota/super-king/cama-box/`
- Fort Comfort Queen — `saidas/produtos/molas/fort-comfort/queen/cama-box/`
- Fort Comfort King — `saidas/produtos/molas/fort-comfort/king/cama-box/`
- Lancaster King — `saidas/produtos/molas/lancaster/king/cama-box/`
- Livorno Queen — `saidas/produtos/molas/livorno/queen/cama-box/`
- Pró Dream Queen — `saidas/produtos/molas/pro-dream/queen/cama-box/`
- Pró Dream King — `saidas/produtos/molas/pro-dream/king/cama-box/`

## Como corrigir

Trocar, em cada arquivo da lista "precisam de correção":

```
De:  01 colch&atilde;o + 01 base
Para: 01 colch&atilde;o + 02 base bipartida
```

É uma troca de texto idêntica nas 23 páginas — posso rodar em lote quando quiser.
