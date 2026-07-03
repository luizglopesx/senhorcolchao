# Meta Ads — Durma como Campeão | Julho 2026
**Conta:** senhor_colchao (act_888195439518063)  
**Objetivo:** Mensagens (CTWA → WhatsApp)  
**Budget aprovado:** R$ 800
**Budget operacional configurado:** até R$ 816 (Fase 1 antecipada para 06/07)
**Estrutura:** 1 campanha → 2 conjuntos → 2 criativos por fase  
**Atualizado em:** 03/07/2026 — Pixel

---

## Aprendizados aplicados

| Problema anterior | O que muda aqui |
|---|---|
| CP04 sem urgência → R$16/conversa | Copy com data de encerramento em todo criativo |
| D33 morreu silencioso, continuou gastando | Pausar criativo se CTR < 0,80% em 3 dias consecutivos |
| CP04 frequência 3,21 — incomodando | Frequência ≥ 3,0 pausa criativo; não sobe budget |
| Copa: 3 conjuntos competindo entre si | 1 campanha, 2 conjuntos, 1 objetivo |
| Copa: frequência alta → aumentaram verba | Saturação = troca criativo, nunca aumenta verba por impulso |
| Raio ampliado além da entrega | Fixo: Barretos + 40 km — saturou: troca criativo, não raio |
| Copa: `end_time 29/06` passado sem perceber | `end_time` obrigatório e verificado antes de ativar |

---

## Estrutura da Campanha

```
Campanha: "Durma como Campeão — Julho 2026"
├── Conjunto 1 — Fase 1 | 06-19/07 | R$30/dia | R$420
│   ├── Anúncio A — Arte 01 (Abertura) — 9:16 + 4:5
│   └── Anúncio B — Arte 02 (Orthoplus R$1.890) — 9:16 + 4:5
│
└── Conjunto 2 — Fase 2 | 20-31/07 | R$33/dia | R$396
    ├── Anúncio A — Arte 04 (Férias) — 9:16 + 4:5
    └── Anúncio B — Arte 05 (Inverno) — 9:16 + 4:5
```

> Arte 03 (SmartFlex R$2.390) fica como reserva. Ativar se algum criativo principal tiver CTR < 0,80% por 3 dias consecutivos ou saturar antes do previsto.
> Como a Fase 1 foi antecipada para 06/07 mantendo R$30/dia, o plano operacional soma R$816 antes de ajustes. Se for necessário respeitar teto estrito de R$800, reduzir a Fase 2 no checkpoint de 18/07.

---

## Conjunto 1 — Fase 1 | Copa/Lançamento (06–19/07)

| Campo | Valor |
|---|---|
| Nome | `Fase 1 \| Copa/Lançamento \| 06-19/07 \| R$30/dia` |
| Objetivo | Mensagens (WhatsApp) |
| Budget diário | R$ 30/dia |
| Total previsto | R$ 420 |
| Início | 06/07/2026 às 08h00 |
| **end_time** | **19/07/2026 às 23h59** ← setar e verificar antes de ativar |
| Público | `LAL 1% \| Leads Copa \| Brasil \| Julho 2026` + interesses: colchões, cama box, móveis, decoração |
| Base de origem | `BASE \| Leads Copa \| Junho/Julho 2026` — 306 linhas carregadas |
| Localização | Barretos SP + 40 km — **não ampliar** |
| Faixa etária | 25–55 anos |
| Dispositivos | Mobile prioritário |
| Posicionamentos | Reels, Stories, Feed (automático Meta Advantage+) |
| Meta CTR | ≥ 1,20% |
| Meta CPC | ≤ R$ 1,10 |
| Meta custo/conversa | ≤ R$ 12,00 |

### Setup registrado — 03/07

- Público personalizado criado por lista: `BASE | Leads Copa | Junho/Julho 2026`
- Lista carregada no Meta: 306 linhas, convertida em hashes e disponível para uso
- Público semelhante criado: `LAL 1% | Leads Copa | Brasil | Julho 2026`
- Status observado: em preenchimento, mas disponível para usar
- Campanha configurada para mensagens no WhatsApp da Senhor Colchão
- Localização do conjunto: Barretos SP + 40 km
- Idade: 25–55
- Início ajustado para segunda-feira, 06/07/2026 às 08h00

### Criativos — Fase 1

**Anúncio A — Arte 01 (Abertura da Campanha)**  
Arquivo: `arte01-abertura-feed.mp4` (4:5) + `arte01-abertura-story.mp4` (9:16)  
Ângulo curto: "Julho chegou. Cama Box com entrega e montagem grátis — só esse mês. ⚠️ Encerra 31/07"

```
Texto principal:
Julho chegou e a Senhor Colchão entrou em campo. 🏆

Esse mês a gente preparou as melhores condições do ano pra você renovar o quarto de vez.

🛏️ Cama Box a partir de R$ 1.890
💳 Em até 12x sem juros
🚚 Entrega grátis
🔧 Montagem grátis — a gente instala no seu quarto

⚠️ Promoção válida só até 31/07. Depois os preços voltam ao normal.

👉 Chama no WhatsApp ou passa na loja — a gente encontra o modelo certo pro seu bolso!

📍 Rua 20, Entre 13x15, 1050
📍 Rua 22, Esq. Av. 9, 1274
```

```
Título: Durma como Campeão este Julho 🏆
Descrição: A partir de R$ 1.890 | 12x sem juros | Entrega + montagem grátis | Só até 31/07
```

---

**Anúncio B — Arte 02 (Orthoplus Casal R$ 1.890)**  
Arquivo: `arte02-orthoplus-feed.mp4` (4:5) + `arte02-orthoplus-story.mp4` (9:16)  
Ângulo curto: "Orthoplus Casal R$1.890 em 12x. Não vai deixar essa passar, né?"

```
Texto principal:
Cama Box Casal Orthoplus por R$ 1.890 em até 12x sem juros. 🛏️✨

Não vai deixar essa passar, né?

✅ Entrega grátis
✅ Montagem grátis — do jeito que você quer, no cômodo que você escolher
✅ Parcelas que cabem no bolso

Essa condição especial existe só em julho. No dia 01/08 o preço muda. ⏳

👉 Chama agora no WhatsApp que a gente resolve na hora!

📍 Rua 20, Entre 13x15, 1050
📍 Rua 22, Esq. Av. 9, 1274
```

```
Título: Cama Box Casal — R$ 1.890 em 12x Sem Juros 🛏️
Descrição: Orthoplus Casal | Entrega + montagem grátis | Condição especial só até 31/07
```

---

## Conjunto 2 — Fase 2 | Férias de Julho (20–31/07)

| Campo | Valor |
|---|---|
| Nome | `Fase 2 \| Férias \| Retarg+LAL \| 20-31/07` |
| Objetivo | Mensagens (WhatsApp) |
| Budget diário | R$ 33/dia |
| Total previsto | R$ 396 |
| Início | 20/07/2026 às 08h00 |
| **end_time** | **31/07/2026 às 23h59** ← setar e verificar antes de ativar |
| Público | Retargeting engajados Fase 1 + Lookalike 1% base geral |
| Localização | Barretos SP + 40 km — **não ampliar** |
| Faixa etária | 25–55 anos |
| Dispositivos | Mobile prioritário |
| Posicionamentos | Reels, Stories, Feed (automático Meta Advantage+) |
| Meta CTR | ≥ 1,20% |
| Meta CPC | ≤ R$ 1,10 |
| Meta custo/conversa | ≤ R$ 12,00 |

### Criativos — Fase 2

**Anúncio A — Arte 04 (Férias de Julho)**  
Arquivo: `arte04-ferias-feed.mp4` (4:5) + `arte04-ferias-story.mp4` (9:16)  
Ângulo curto: "Férias é pra descansar de verdade. Renova o quarto. ⚠️ Encerra 31/07"

```
Texto principal:
Férias é pra descansar de verdade. 🏖️🛏️

A família vai estar em casa — e o quarto vai ser o coração da casa esse julho.

É agora o momento certo pra renovar o que realmente importa.

🛏️ Cama Box + Cabeceira a partir de R$ 1.890
💳 Em até 12x sem juros
🚚 Entrega grátis
🔧 Montagem grátis — você não precisa fazer nada

⚠️ Oferta de férias encerra em 31/07. Não deixa pra última hora!

👉 Chama no WhatsApp ou passa em uma das nossas lojas!

📍 Rua 20, Entre 13x15, 1050
📍 Rua 22, Esq. Av. 9, 1274
```

```
Título: Férias Merece Cama Nova — A partir de R$ 1.890 🏖️
Descrição: Cama Box + Cabeceira | 12x sem juros | Entrega + montagem grátis | Encerra 31/07
```

---

**Anúncio B — Arte 05 (Inverno)**  
Arquivo: `arte05-inverno-feed.mp4` (4:5) + `arte05-inverno-story.mp4` (9:16)  
Ângulo curto: "Tá frio lá fora. Quem tem colchão bom não reclama do inverno."

```
Texto principal:
Tá frio lá fora. ❄️🥶

Mas quem tem um colchão bom não reclama do inverno.

A cama certa faz toda a diferença — você sente na primeira noite.

🛏️ Cama Box a partir de R$ 1.890
💳 Em até 12x sem juros
🚚 Entrega grátis
🔧 Montagem grátis

Não espera o inverno acabar pra trocar. Condição especial de julho encerra em 31/07. ⏳

👉 Chama no WhatsApp ou passa pra ver pessoalmente!

📍 Rua 20, Entre 13x15, 1050
📍 Rua 22, Esq. Av. 9, 1274
```

```
Título: Inverno + Cama Nova = Sono Perfeito ❄️
Descrição: A partir de R$ 1.890 | 12x sem juros | Entrega + montagem grátis | Só até 31/07
```

---

## Criativo Reserva — Arte 03 | SmartFlex Queen R$ 2.390

Arquivo: `arte03-smartflex-feed.mp4` (4:5) + `arte03-smartflex-story.mp4` (9:16)  
Ativar como anúncio reserva se algum criativo principal tiver CTR < 0,80% por 3 dias consecutivos, frequência ≥ 3,0 ou queda clara de conversas.

```
Texto principal:
Sabe aquela sensação de afundar na cama e não querer sair? 😴💤

É exatamente isso que a SmartFlex Queen entrega.

🌀 Molas ensacadas — isola o movimento do outro lado da cama
📏 30cm de conforto real
💳 R$ 2.390 em até 12x sem juros
🚚 Entrega grátis
🔧 Montagem grátis

Tecnologia que vale cada centavo — e em julho tá com condições especiais que não voltam tão cedo. ⚠️ Encerra 31/07.

👉 Chama no WhatsApp ou passa pra sentir de perto!

📍 Rua 20, Entre 13x15, 1050
📍 Rua 22, Esq. Av. 9, 1274
```

```
Título: SmartFlex Queen — Molas Ensacadas por R$ 2.390 😴
Descrição: 30cm de conforto | 12x sem juros | Entrega + montagem grátis | Só até 31/07
```

---

## Resumo de Budget

| Fase | Período | Dias | Budget/dia | Total |
|---|---|---:|---:|---:|
| Fase 1 — Copa/Lançamento | 06–19/07 | 14 | R$ 30 | R$ 420 |
| Fase 2 — Férias de Julho | 20–31/07 | 12 | R$ 33 | R$ 396 |
| Buffer overdelivery planejado | — | — | — | R$ 0 |
| **Total operacional** | | | | **R$ 816** |

> Budget aprovado original: R$800. A antecipação para 06/07 adiciona R$30 na Fase 1; compensar na Fase 2 se o controle financeiro exigir teto estrito.

---

## Regras Inegociáveis

### Setup
- **end_time setado nos dois conjuntos antes de ativar**
- Conferir `end_time` da Fase 1: **19/07/2026 às 23h59**
- Conferir `end_time` da Fase 2: **31/07/2026 às 23h59**
- Localização fixa: **Barretos SP + 40 km**

### Frequência
| Frequência | Ação |
|---|---|
| ≥ 2,5 | Reduzir budget diário em 25% e observar por 24h |
| ≥ 3,0 | Pausar criativo atual e ativar próximo da fila |
| ≥ 4,0 | Pausar conjunto — público esgotado |

### Criativos
| Indicador | Ação |
|---|---|
| CTR < 0,80% por 3 dias | Pausar criativo e ativar Arte 03 (SmartFlex) |
| 0 conversas em 3 dias com gasto > R$ 30 | Pausar criativo |
| Custo/conversa > R$ 15 por 2 dias | Revisar público + criativo |

### Budget e Público
- **Frequência ≥ 3,0 → pausa criativo, não sobe budget**
- **Saturou área → troca criativo, nunca amplia raio**
- **Nunca aumentar budget quando frequência está subindo**
- Se custo/dia < R$ 20 por 2 dias → checar se `end_time` não expirou

---

## Checkpoints Obrigatórios

| Data | O que verificar |
|---|---|
| 09/07 (3 dias de veiculação) | CTR, CPC, custo/conversa, frequência de cada criativo |
| 18/07 (véspera da virada) | Decidir se mantém R$ 33/dia na Fase 2 ou ajusta |
| 23/07 (3 dias da Fase 2) | Mesmas métricas + checar retargeting vs LAL separado |
| 28/07 | Frequência — se ≥ 2,5 reduzir para R$ 20/dia até 31/07 |

---

## Contingência Copa

| Cenário | Ação |
|---|---|
| Brasil passa 05/07 | Ativar versões Copa standby nas artes 01 e 02 antes de subir os anúncios |
| Brasil cai antes de 19/07 | Trocar imediatamente Arte 01 + 02 pela Arte 04 (férias) — manter end_time 19/07 |
| Brasil cai e é antes de 14/07 | Antecipar Fase 2 para data da eliminação |

---

*Atualizado em: 03/07/2026 — Pixel*
