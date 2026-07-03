# Meta Ads — Durma como Campeão | Julho 2026
**Conta:** senhor_colchao (act_888195439518063)  
**Objetivo:** Mensagens (CTWA → WhatsApp)  
**Budget total:** R$ 800  
**Gerado em:** 03/07/2026 — Pixel

---

## Aprendizados aplicados

| Problema anterior | O que muda aqui |
|---|---|
| CP04 sem urgência → R$16/conversa | Copy com data de encerramento em todo criativo |
| D33 morreu silencioso, continuou gastando | Pausar criativo se CTR < 0,80% em 3 dias consecutivos |
| CP04 frequência 3,21 — incomodando | Alerta em 2,5 → reduz budget; 3,0 → pausa e troca criativo |
| Copa: 3 conjuntos competindo entre si | 1 conjunto por fase, 1 objetivo |
| Copa: frequência alta → aumentaram verba | Saturação = reduz budget, nunca aumenta |
| Raio ampliado além da entrega | Fixo: Barretos + 40 km — saturou: troca criativo, não raio |
| Copa: `end_time 29/06` passado sem perceber | `end_time` obrigatório e verificado antes de ativar |

---

## Estrutura da Campanha

```
Campanha: "Durma como Campeão — Julho 2026"
├── Conjunto 1 — Fase 1 | Copa | Lookalike | 07-19/07  (R$30/dia)
│   ├── Anúncio A — Arte 01 (Abertura) — 9:16 + 4:5
│   └── Anúncio B — Arte 02 (Orthoplus R$1.890) — 9:16 + 4:5
│
└── Conjunto 2 — Fase 2 | Férias | Retarg+LAL | 20-31/07  (R$33/dia)
    ├── Anúncio A — Arte 04 (Férias) — 9:16 + 4:5
    └── Anúncio B — Arte 05 (Inverno) — 9:16 + 4:5
```

> Arte 03 (SmartFlex R$2.390) entra como anúncio C em qualquer fase se algum dos 2 principais saturar antes do previsto.

---

## Conjunto 1 — Fase 1 | Copa/Lançamento (07–19/07)

| Campo | Valor |
|---|---|
| Nome | `Fase 1 \| Copa \| Lookalike \| 07-19/07` |
| Objetivo | Mensagens (WhatsApp) |
| Budget diário | R$ 30/dia |
| Início | 07/07/2026 às 08h00 |
| **end_time** | **19/07/2026 às 23h59** ← obrigatório, verificar antes de ativar |
| Público | Lookalike 1% base Copa + interesses: colchões, cama box, móveis, decoração |
| Localização | Barretos SP + 40 km — **não ampliar** |
| Faixa etária | 25–55 anos |
| Dispositivos | Mobile prioritário |
| Posicionamentos | Reels, Stories, Feed (automático Meta Advantage+) |
| Meta CTR | ≥ 1,20% |
| Meta CPC | ≤ R$ 1,10 |
| Meta custo/conversa | ≤ R$ 12,00 |

### Criativos — Fase 1

**Anúncio A — Arte 01 (Abertura)**  
Arquivo: `arte01-abertura-feed.mp4` (4:5) + `arte01-abertura-story.mp4` (9:16)

```
Texto primário:
Julho chegou e a Senhor Colchão entrou em campo. 🏆

Cama Box com entrega e montagem grátis — condições que só têm esse mês.

✓ A partir de R$ 1.890 em até 12x sem juros
✓ Entrega grátis
✓ Montagem grátis

⚠️ Promoção válida até 31/07. Depois os preços voltam ao normal.

👉 Chama no WhatsApp e descobre o modelo certo pro seu bolso.
```

```
Headline: Durma como Campeão este Julho 🏆
Descrição: Cama Box a partir de R$1.890 | 12x sem juros | Entrega + montagem grátis
```

---

**Anúncio B — Arte 02 (Orthoplus R$1.890)**  
Arquivo: `arte02-orthoplus-feed.mp4` (4:5) + `arte02-orthoplus-story.mp4` (9:16)

```
Texto primário:
Cama Box Casal Orthoplus por R$ 1.890 em até 12x sem juros. 🛏️

✓ Entrega grátis
✓ Montagem grátis — a gente instala no seu quarto

Não vai deixar essa passar, né? Essa condição especial encerra em 31/07.

👉 Chama agora no WhatsApp — a gente resolve na hora!
```

```
Headline: Cama Box Casal — R$ 1.890 em 12x Sem Juros
Descrição: Orthoplus Casal | Entrega + montagem grátis | Só até 31/07
```

---

## Conjunto 2 — Fase 2 | Férias de Julho (20–31/07)

| Campo | Valor |
|---|---|
| Nome | `Fase 2 \| Férias \| Retarg+LAL \| 20-31/07` |
| Objetivo | Mensagens (WhatsApp) |
| Budget diário | R$ 33/dia |
| Início | 20/07/2026 às 08h00 |
| **end_time** | **31/07/2026 às 23h59** ← obrigatório, verificar antes de ativar |
| Público | Retargeting engajados Fase 1 (clicaram/interagiram 07–19/07) + Lookalike 1% base geral |
| Localização | Barretos SP + 40 km — **não ampliar** |
| Faixa etária | 25–55 anos |
| Dispositivos | Mobile prioritário |
| Posicionamentos | Reels, Stories, Feed (automático Meta Advantage+) |
| Meta CTR | ≥ 1,20% |
| Meta CPC | ≤ R$ 1,10 |
| Meta custo/conversa | ≤ R$ 12,00 |

### Criativos — Fase 2

**Anúncio A — Arte 04 (Férias)**  
Arquivo: `arte04-ferias-feed.mp4` (4:5) + `arte04-ferias-story.mp4` (9:16)

```
Texto primário:
Férias é pra descansar de verdade. Não dá pra relaxar numa cama velha. 🏠

A família vai estar em casa — é o momento certo de renovar o quarto.

Colchão + Box + Cabeceira com entrega e montagem grátis.
A partir de R$ 1.890 em até 12x sem juros.

⚠️ Oferta de julho encerra em 31/07. Depois é preço cheio.

👉 Chama no WhatsApp agora!
```

```
Headline: Férias Merece Cama Nova 🛏️
Descrição: A partir de R$1.890 | 12x sem juros | Entrega + montagem grátis | Encerra 31/07
```

---

**Anúncio B — Arte 05 (Inverno)**  
Arquivo: `arte05-inverno-feed.mp4` (4:5) + `arte05-inverno-story.mp4` (9:16)

```
Texto primário:
Tá frio lá fora. ❄️

Mas quem tem um colchão bom não reclama do inverno.

Troca agora e sente a diferença na primeira noite. Cama Box com entrega e montagem grátis — condições especiais só em julho.

A partir de R$ 1.890 em até 12x sem juros.

⚠️ Encerra 31/07.

👉 Chama no WhatsApp!
```

```
Headline: Inverno + Cama Nova = Sono Perfeito ❄️
Descrição: A partir de R$1.890 | 12x sem juros | Entrega + montagem grátis | Só em julho
```

---

**Anúncio C — Arte 03 (SmartFlex) — reserva**  
Arquivo: `arte03-smartflex-feed.mp4` (4:5) + `arte03-smartflex-story.mp4` (9:16)  
*Ativar se A ou B tiver CTR < 0,80% por 3 dias consecutivos*

```
Texto primário:
Sono de verdade começa numa cama de qualidade. 😴

Cama Box Queen SmartFlex — molas ensacadas que isolam o movimento do outro lado.
30 cm de conforto real.

R$ 2.390 em até 12x sem juros.

✓ Entrega grátis
✓ Montagem grátis

⚠️ Condição especial de julho — encerra 31/07.

👉 Chama no WhatsApp!
```

```
Headline: SmartFlex Queen — Molas Ensacadas R$ 2.390
Descrição: 30cm de conforto | 12x sem juros | Entrega + montagem grátis | Só julho
```

---

## Resumo de Budget

| Fase | Período | Dias | Budget/dia | Total |
|---|---|---|---|---|
| Fase 1 — Copa/Lançamento | 07–19/07 | 13 | R$ 30 | R$ 390 |
| Fase 2 — Férias de Julho | 20–31/07 | 12 | R$ 33 | R$ 396 |
| Buffer overdelivery | — | — | — | R$ 14 |
| **Total** | | | | **R$ 800** |

---

## Regras de Gestão (obrigatórias)

### Frequência
| Frequência | Ação |
|---|---|
| ≥ 2,5 | Reduzir budget diário em 25% |
| ≥ 3,0 | Pausar criativo atual e ativar próximo da fila |
| ≥ 4,0 | Pausar conjunto — público esgotado |

### Criativos
| Indicador | Ação |
|---|---|
| CTR < 0,80% por 3 dias | Pausar criativo, ativar reserva (Arte 03) |
| 0 conversas em 3 dias com gasto > R$ 30 | Pausar criativo |
| Custo/conversa > R$ 15 por 2 dias | Revisar público + criativo |

### Budget
- **Nunca aumentar** budget quando frequência está subindo
- **Nunca ampliar raio** geográfico — saturou: troca criativo
- Se custo/dia < R$ 20 por 2 dias → checar se end_time não expirou

### Checkpoints obrigatórios
| Data | O que verificar |
|---|---|
| 10/07 (3 dias de veiculação) | CTR, CPC, custo/conversa, frequência de cada criativo |
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

*Gerado em: 03/07/2026 — Pixel*
