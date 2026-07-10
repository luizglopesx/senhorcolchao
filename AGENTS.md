# Senhor Colchao — Instrucoes para agentes

Este projeto e o MazyOS da Senhor Colchao Sleep Store. A memoria oficial e portavel fica em arquivos Markdown dentro do proprio repositorio, principalmente em `_memoria/`.

Use este arquivo como guia para Codex e outros agentes que nao leem `CLAUDE.md` automaticamente.

---

## Contexto Que Deve Ser Considerado

Ao iniciar uma tarefa neste repositorio, leia quando for relevante:

1. `_memoria/empresa.md` — quem e a empresa, equipe, operacao, canais e contexto geral
2. `_memoria/preferencias.md` — tom de voz, estilo de escrita, termos a evitar
3. `_memoria/estrategia.md` — foco atual, campanhas, prioridades e aprendizados recentes
4. `_memoria/campanhas-meta-ads.md` — aprendizados especificos de Meta Ads, quando a tarefa envolver midia paga
5. `CLAUDE.md` — regras historicas do MazyOS e organizacao do projeto
6. `identidade/design-guide.md` — quando a tarefa envolver visual, layout, post, landing page ou criativo

Nao precisa listar que esses arquivos foram lidos. Use o contexto naturalmente.

---

## Como Falar Pela Marca

Tom de voz da Senhor Colchao:

- Direto, acolhedor e sem frescura
- Como um vizinho especialista em sono
- Frases curtas
- Oferta em destaque logo no inicio
- CTA claro: "chama no WhatsApp", "passa na loja", "vem conhecer"

Evitar:

- "vamos juntos"
- "alavancar"
- "sinergia"
- "potencializar"
- "caro cliente"
- "prezado consumidor"
- Promessas vagas como "o melhor da cidade"
- Excesso de emojis

Quando houver oferta, valorizar:

- Entrega gratis
- Montagem gratis
- Parcelamento
- Desconto/urgencia real
- Produto e tamanho com clareza

---

## Organizacao De Arquivos

- Conteudo e planejamento de marketing: `marketing/`
- Relatorios de campanha: `marketing/campanhas/relatorios/`
- Entregaveis pontuais: `saidas/`
- Arquivos de entrada para analise: `dados/`
- Memoria do negocio: `_memoria/`
- Marca e referencias visuais: `identidade/`
- Scripts e automacoes: `scripts/`
- Publicacao Instagram/GitHub Actions: `instagram/` e `.github/workflows/`
- Paginas de produto Simplo 7: `saidas/produtos/<produto>/`
- Templates reutilizaveis (skills, perfis, ferramentas, identidade): `templates/`

Nao salvar dados sensiveis de clientes, telefones, tokens, credenciais ou exports com PII em arquivos versionados. CSVs de clientes devem ficar fora do Git.

---

## Comando `/atualizar`

Quando o usuario escrever `/atualizar`, `atualizar memoria`, `varrer projeto`, `atualiza o MazyOS` ou algo equivalente, execute este fluxo:

### 1. Levantamento

Verifique:

- Estrutura de pastas da raiz
- Arquivos recentes em `marketing/`, `saidas/`, `scripts/`, `instagram/`, `dados/`
- Campanhas ativas e planejamentos recentes
- Relatorios recentes
- Scripts novos
- Mudancas em ferramentas, canais, automacoes e APIs
- Arquivos de contexto existentes em `_memoria/`
- Regras atuais em `CLAUDE.md` e `AGENTS.md`

### 2. Comparacao

Compare o estado real do workspace com:

- `_memoria/empresa.md`
- `_memoria/preferencias.md`
- `_memoria/estrategia.md`
- `_memoria/campanhas-meta-ads.md`
- `CLAUDE.md`
- `AGENTS.md`
- `identidade/design-guide.md`, quando houver impacto visual

Procure inconsistencias como:

- Campanha marcada como planejada, mas ja lancada
- Datas antigas
- Metas ou budgets alterados
- Ferramentas novas ainda nao registradas
- Aprendizados de atendimento ou midia paga nao salvos
- Regras de pasta desatualizadas
- Preferencias do Luiz que foram repetidas em conversa, mas nao estao na memoria

### 3. Proposta

Antes de editar, apresente uma lista curta:

```text
Encontrei [N] coisas pra atualizar:

1. _memoria/estrategia.md — campanha X mudou de planejada para ativa.
2. _memoria/campanhas-meta-ads.md — novo aprendizado sobre CTR/frequencia.
3. AGENTS.md — regra de organizacao Y precisa refletir a pratica atual.

Quer que eu aplique todas, algumas ou nenhuma?
```

Se o usuario disser claramente "pode salvar", "salve", "aplique" ou "faz", aplique sem nova confirmacao.

### 4. Aplicacao

Ao editar:

- Fazer cirurgia pequena
- Nao reformatar o arquivo inteiro
- Nao apagar memoria antiga sem necessidade
- Registrar apenas fatos com evidencia no workspace ou confirmados pelo usuario
- Se a evidencia for ambigua, perguntar antes
- Depois, mostrar resumo do que mudou

---

## Quando O Usuario Disser "Salve Isso"

Salvar em `_memoria/` ou nos arquivos de instrucao conforme o tipo:

- Sobre empresa, equipe, operacao, lojas, canais: `_memoria/empresa.md`
- Preferencias de escrita, tom, linguagem, termos a evitar: `_memoria/preferencias.md`
- Prioridades, campanhas, metas, prazos, foco atual: `_memoria/estrategia.md`
- Aprendizados de Meta Ads, Google Ads, campanhas, benchmarks: `_memoria/campanhas-meta-ads.md`
- Regras permanentes do projeto para Codex/agentes: `AGENTS.md`
- Regras permanentes tambem usadas pelo Claude Code/MazyOS: `CLAUDE.md`
- Design, layout, marca, padroes visuais: `identidade/design-guide.md`

Se o usuario pedir "salve na memoria", escolha o arquivo mais adequado e explique rapidamente onde salvou.

Nao salvar:

- Telefones de clientes
- Nomes de clientes individuais vindos de CSV/export
- Tokens, chaves, credenciais, senhas
- Dados financeiros sensiveis que nao sejam agregados ou ja estejam em relatorios do projeto

---

## Aprender Com Correcoes

Quando o usuario corrigir algo de forma permanente, por exemplo:

- "nao fala assim"
- "prefiro desse jeito"
- "sempre usa esse formato"
- "isso aqui e regra"
- "a partir de agora..."

Pergunte:

```text
Quer que eu salve isso na memoria pra nao precisar repetir?
```

Se ele confirmar, salve no arquivo certo.

---

## Ferramentas E Integracoes

O projeto usa ou referencia:

- Meta Ads API
- Meta/Instagram via GitHub Actions
- Google Ads API
- Campaign Manager para atendimento WhatsApp
- Simplo 7 para e-commerce
- Gmail, Google Calendar e Google Drive via MCP (conectores claude.ai)
- Receitas Manager para financeiro (fluxo de caixa, contas, DRE)
- Supabase (bucket `catalogo`) para imagens de produto

Credenciais ficam no `.env`, que nao deve ser versionado nem exibido em respostas.

Ao usar APIs:

- Nao imprimir tokens
- Resumir resultados
- Conferir datas absolutas
- Registrar aprendizados relevantes em `_memoria/` quando o usuario pedir

---

## Git

Antes de commitar:

- Rodar `git status --short`
- Conferir diff
- Evitar incluir CSVs de clientes, `.env`, exports com telefone ou dados pessoais
- Fazer commit com mensagem curta e clara quando o usuario pedir commit/salvar no Git

Se o usuario pedir push, fazer push depois do commit.

---

## Relacao Com `CLAUDE.md`

`CLAUDE.md` continua sendo a referencia principal para Claude Code/MazyOS.

`AGENTS.md` e a referencia principal para Codex e outros agentes.

Os dois devem apontar para a mesma memoria portavel em `_memoria/`. Quando uma regra permanente mudar, manter ambos coerentes quando fizer sentido.
