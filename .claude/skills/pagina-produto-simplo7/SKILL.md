---
name: pagina-produto-simplo7
description: "Cria ou revisa paginas HTML de descricao de produtos no Simplo7, incluindo colchao avulso, cama box e variacoes por tamanho/altura. Localiza e valida imagens no Supabase, confirma dados na pagina publica ou em arquivos existentes, organiza as pastas do catalogo, monta o layout padrao e entrega obrigatoriamente os campos de SEO. Use quando o usuario pedir pagina de produto, HTML de produto, descricao Simplo7, cadastro de colchao, variacao de tamanho ou altura, ou os campos SEO de um produto."
---

# Pagina de Produto Simplo7

Criar a descricao HTML e o bloco de SEO pronto para copiar no cadastro do produto. Nunca inventar especificacoes, imagens, marca, garantia, suporte de peso ou oferta.

## Fontes e ordem de confianca

1. Dados confirmados pelo usuario na conversa.
2. Pagina publica do produto (informada pelo usuario ou localizada pela categoria do site quando o usuario nao passar o link).
3. HTML existente do mesmo produto ou de outra medida da mesma linha — usar so para layout/estrutura; nunca para copiar conforto, suporte de peso, garantia ou tratamento sem confirmar na fonte 2.
4. Produto equivalente no catalogo, apenas para estrutura visual; nao copiar dados tecnicos sem confirmacao.

Mesmo quando ja existe HTML de outra medida da mesma linha (ex: pasta ja criada, variacao irma), abrir a pagina publica da medida especifica sendo criada antes de escrever qualquer dado tecnico. Cada variacao pode ter conforto, suporte de peso ou garantia diferentes — nao presumir que sao iguais so porque a linha e a mesma. Se o usuario nao informar a URL, localizar o produto na pagina de categoria do site (ex: `/colchao-espuma/<tamanho>`) antes de recorrer ao HTML existente como unica fonte.

Consultar `identidade/design-guide.md`, `_memoria/preferencias.md` e o HTML aprovado mais proximo. Para cama box, ler tambem `../pagina-cama-box/SKILL.md`.

## Workflow

1. Confirmar produto, tipo, tamanho completo, altura, marca e variacoes que diferenciam o cadastro.
2. Abrir a pagina publica da medida especifica (URL do usuario ou localizada na categoria do site) e extrair: nome, composicao, conforto, tecido, tratamento, suporte, medidas, cor, conteudo e garantia. Fazer isso mesmo se ja existir HTML de outra medida da mesma linha — nao presumir que os dados tecnicos se repetem entre variacoes.
3. Localizar a pasta real em `products/` no bucket Supabase. Listar os arquivos antes de montar URLs; nao presumir nomes.
4. Preferir foto de cena no Hero e foto de estudio em Medidas. Se faltar o tamanho exato, usar imagem da mesma linha como fallback e avisar claramente.
5. Validar cada URL publica de imagem; aceitar somente resposta HTTP 200.
6. Criar ou revisar o HTML seguindo o padrao visual das paginas aprovadas: Hero, beneficios, composicao/produto, ficha tecnica, medidas, aviso de entrega e CTA. Cama box inclui as secoes de colchao e base.
7. Salvar em `saidas/produtos/<categoria>/<produto>/<variacao>/<tipo>/descricao-simplo7-<produto>-<variacao>-<tipo>.html`.
8. Gerar e entregar o bloco obrigatorio de SEO e atributos tecnicos descrito abaixo.
9. Validar tags balanceadas, ausencia de dados da variante usada como base, URLs codificadas e `git diff --check`.

## Organizacao das variacoes

- Separar em pastas diferentes todos os produtos com largura, comprimento ou altura diferentes.
- Incluir a altura na pasta e no nome do HTML quando a mesma linha tiver mais de uma altura: `solteiro-88-18cm`, `solteiro-88-25cm`.
- Nao sobrescrever uma variacao para criar outra.
- Se reorganizar um arquivo antigo, remover somente as pastas antigas que ficarem vazias.

## HTML e texto

- Usar estilos inline e tabelas compatíveis com o editor do Simplo7.
- Usar as cores aprovadas: azul `#001da4`, amarelo `#f7cf00` e os neutros ja usados no catalogo.
- Escrever de forma direta, acolhedora e concreta.
- Destacar entrega gratis quando confirmada. Mencionar montagem gratis apenas quando aplicavel.
- Nao usar promessas vagas, superioridade sem prova ou comparacoes tecnicas nao confirmadas.
- Codificar acentos como entidades HTML quando o padrao do arquivo exigir.
- Codificar integralmente a mensagem do link do WhatsApp.

### Ficha tecnica

- No campo `Revestimento`, informar somente o tecido ou material de revestimento. Nao incluir `base antiderrapante` nesse campo.
- No campo `Suporte`, informar somente o limite de peso por pessoa, por exemplo: `Ate 150 kg por pessoa`. Nao acrescentar condicionais de altura ou outros detalhes nesse campo.

## SEO obrigatorio para cada produto

Entregar sempre, mesmo que o usuario tenha pedido apenas o HTML:

```text
Meta Title: ...
Meta Description: ...
Tag H1: ...
Meta Keywords: deixar em branco
```

### Meta Title

- Criar titulo unico, descritivo e natural, normalmente entre 50 e 60 caracteres.
- Priorizar: tipo/tamanho + densidade ou tecnologia + modelo + medida completa.
- Colocar `| Senhor Colchao` no final quando couber sem prejudicar os termos principais.
- Usar caixa normal; nunca escrever tudo em maiusculas.
- Nao repetir palavras para tentar ranquear.

Exemplo:

```text
Colchao Solteiro D65 Orthoplus 88x188x25 | Senhor Colchao
```

### Meta Description

- Criar descricao unica e humana, de preferencia entre 140 e 160 caracteres.
- Reunir produto, medida, conforto/composicao, suporte de peso, diferencial real, entrega local e CTA.
- Usar `Entrega gratis em Barretos e regiao` apenas quando a condicao estiver confirmada.
- Nao usar textos genericos como `os menores precos`, `o melhor da cidade` ou `qualidade incomparavel`.
- Nao transformar a descricao em uma lista de palavras-chave.

### Tag H1

- Preencher; nao deixar o CMS escolher um nome incompleto.
- Usar um unico nome principal, legivel e coerente com o Meta Title e com o titulo visivel.
- Incluir tamanho, densidade/tecnologia, modelo e medida quando relevantes.

### Meta Keywords

- Deixar em branco. O Google nao usa essa tag para indexacao ou ranking.

Se o CMS tiver um grupo `Colchoes`, `Cama Box` ou equivalente, recomendar o grupo correto. Nao afirmar que os atributos geram dados estruturados sem verificar o HTML publicado.

## Alinhamento com Google Ads

- Consultar os relatorios recentes em `marketing/campanhas/relatorios/` quando houver termos de busca reais relevantes.
- Usar na pagina termos especificos que correspondam ao produto, como `colchao solteiro`, densidade e medida.
- Direcionar buscas especificas para a pagina exata do produto. Reservar termos genericos, como `comprar colchao de espuma`, para paginas de categoria quando fizer mais sentido.
- Nao encher todas as paginas com a mesma keyword.
- Usar sempre a URL final sem `www` nos anuncios enquanto o redirecionamento com `www` continuar descartando `gclid` e UTMs.
- Tratar SEO como parte da relevancia. Nao prometer melhora de CPC ou Quality Score apenas por alterar metatags; conteudo visivel, utilidade, navegacao e velocidade tambem importam.

## Entrega final

Informar:

1. Link do HTML criado ou revisado.
2. Fallbacks de imagem ou dados que nao puderam ser confirmados.
3. Bloco completo de SEO pronto para copiar.
4. Resultado das validacoes.
5. Nao fazer commit, salvo pedido explicito.
