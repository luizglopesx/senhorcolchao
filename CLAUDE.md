# Senhor Colchão Sleep Store — MazyOS

Operação da Senhor Colchão Sleep Store. Empresa familiar de varejo de produtos para descanso (colchões, cama box, box baú, cabeceiras). O sistema gira em torno de marketing, vendas e gestão financeira do dia a dia.

**Estrutura de pastas:**
- `_memoria/` — quem é a empresa, como falamos, foco atual
- `identidade/` — marca aplicada em tudo que o sistema gera
- `marketing/` — campanhas, conteúdo, mídia paga
- `saidas/` — documentos e entregáveis pontuais
- `dados/` — arquivos a analisar
- `scripts/` — automações e scripts de apoio
- `instagram/` — automação de publicação no Instagram via GitHub Actions (`.github/workflows/`)

---

## Contexto do negócio

No início de toda conversa, ler os seguintes arquivos (quando existirem e estiverem preenchidos):

1. `_memoria/empresa.md` — quem é o usuário, o que faz, como funciona o negócio
2. `_memoria/preferencias.md` — tom de voz, estilo de escrita, o que evitar
3. `_memoria/estrategia.md` — foco atual, prioridades, prazos

Usar essas informações como base pra qualquer resposta ou decisão. Ao sugerir prioridades, formatos ou abordagens, considerar o foco atual descrito em `estrategia.md`.

Pra qualquer tarefa visual (carrossel, post, landing page), consultar `identidade/design-guide.md` como referência de estilo.

Não é necessário listar o que foi lido nem confirmar a leitura. Apenas usar o contexto naturalmente.

---

## Sobre a empresa

Senhor Colchão Sleep Store é um comércio varejista de produtos para descanso. Atua no segmento de colchões, cama box, box baú e cabeceiras, atendendo clientes entre 25 e 65 anos em diferentes fases de vida. Somos 6 pessoas — família + equipe de entrega.

## Setores e responsáveis

- **Gestão geral:** Luiz Gustavo (decisões gerais, marketing, entregas, salários)
- **Vendas:** Pai (vendas presenciais e decisões comerciais)
- **Marketing:** Filho (produção de peças visuais)
- **Entregas:** 2 colaboradores (entrega e montagem)

## O que mais fazemos aqui

- Campanhas de marketing e promoções sazonais para girar estoque
- Gestão financeira diária (boletos, antecipações, saldo)
- Conteúdo para Instagram e Facebook
- Atendimento via WhatsApp e presencial

## Tom de voz

Direto, acolhedor e sem frescura. Escreve como um vizinho que entende muito de sono — não empurra, não exagera, não usa jargão. Frases curtas, CTA claro, oferta em destaque logo no início.

Evitar: "vamos juntos!", "alavancar", "sinergia", "caro cliente", excesso de emojis, linguagem formal.

## Regras do sistema

- Conteúdo de marketing salvar em `marketing/`
- Entregáveis pontuais (emails, textos avulsos) salvar em `saidas/`
- Dados e planilhas a analisar colocar em `dados/`
- Logo e arquivos visuais em `identidade/`
- Páginas de produto (Simplo 7) salvar em `saidas/produtos/<produto>/` — pasta nomeada pelo produto, com o mockup, as imagens e o código de produção dentro

## Ferramentas conectadas

- [ ] Gmail
- [ ] Google Calendar
- [x] Google Ads — leitura/edição/otimização via API (v21); credenciais GOOGLE_ADS_* no `.env`
- [x] Meta Ads API — insights e edição de campanhas via `meta_ads_client.py` (`.claude/skills/social-post-scheduler/scripts/`)
- [x] Meta / Instagram — postagem automatizada via GitHub Actions (`.github/workflows/`)
- [x] Campaign Manager — atendimento WhatsApp via API; credenciais CAMPAIGN_MANAGER_* no `.env`

*(Marcar conforme for instalando os MCPs)*

---

## Fluxo de trabalho

Antes de executar qualquer tarefa, verificar se existe skill relevante em `.claude/skills/`. Se encontrar, seguir as instruções da skill. Se não encontrar, executar a tarefa normalmente.

Ao concluir uma tarefa que não tinha skill mas parece repetível, perguntar:

> "Isso pode virar uma skill pra próxima vez. Quer que eu crie?"

---

## Aprender com correções

Quando o usuário corrigir algo ou dar instrução permanente ("na verdade é assim", "não faça mais isso", "prefiro assim", "sempre que...", "evita..."), perguntar:

> "Quer que eu salve isso pra não precisar repetir?"

Se sim, identificar onde faz mais sentido salvar:

- **Sobre o negócio** → `_memoria/empresa.md`
- **Sobre preferências e estilo** → `_memoria/preferencias.md`
- **Sobre prioridades e foco** → `_memoria/estrategia.md`
- **Regra de comportamento nessa pasta** → próprio `CLAUDE.md`

---

## Manter contexto atualizado

Ao terminar uma tarefa que mudou algo relevante, perguntar:

> "Isso mudou algo no teu contexto. Quer que eu atualize a memória?"

**Quando NÃO perguntar:**
- Tarefas pontuais sem impacto no contexto
- Perguntas simples ou conversas sem ação

**Dica:** rode `/atualizar` pra uma varredura completa quando houver dúvida.

---

## Criação de skills

Quando o usuário pedir skill nova:

1. Verificar se existe template relevante em `templates/skills/`
2. Perguntar se é específica desse projeto ou útil em qualquer projeto
3. Ler `_memoria/empresa.md` e `_memoria/preferencias.md` pra calibrar o conteúdo
4. Seguir o fluxo da skill-creator nativa do Claude Code
