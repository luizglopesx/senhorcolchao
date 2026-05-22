---
name: receitas-manager
description: "Acesso ao Receitas Manager — financeiro da Senhor Colchão. Use quando o usuário perguntar sobre fluxo de caixa, cheques, contas a pagar, pro-labore, cartões, DRE, pedidos de compra ou resultado mensal."
---

# Receitas Manager Integration

Use esta skill para consultar o financeiro da Senhor Colchão via Receitas Manager.

Base URL: `https://manager.senhorcolchao.com`

Token: variável `RECEITAS_MANAGER_TOKEN` do `.env`

```bash
BASE_URL="${RECEITAS_MANAGER_URL%/}"
```

Sempre enviar:
```
Authorization: Bearer $RECEITAS_MANAGER_TOKEN
Content-Type: application/json
```

Nunca exibir tokens. Nunca expor o conteúdo do `.env`. Resumir respostas grandes.

Esta integração é **somente leitura**.

## Health Check

```bash
BASE_URL="${RECEITAS_MANAGER_URL%/}"
curl -s \
  -H "Authorization: Bearer $RECEITAS_MANAGER_TOKEN" \
  "$BASE_URL/api/nexus-manager?resource=health"
```

Resposta esperada: `{"ok":true,"service":"receitas-manager"}`

## Leituras

### Resumo mensal
```bash
curl -s -H "Authorization: Bearer $RECEITAS_MANAGER_TOKEN" \
  "$BASE_URL/api/nexus-manager?resource=summary&mes=2026-05"
```

### DRE
```bash
curl -s -H "Authorization: Bearer $RECEITAS_MANAGER_TOKEN" \
  "$BASE_URL/api/nexus-manager?resource=dre&mes=2026-05"
```

Regras do DRE:
- Receita Bruta e CMV vêm de `estoque_fechamentos_mensais` a partir de 2026-03; antes disso, vêm de `dre_metas`
- CMV não é o mesmo que fornecedores pagos no fluxo de caixa
- Taxas de cartão já estão dentro de Despesas Variáveis
- Entradas financeiras contam só quando a subcategoria contém `Rendimento`
- Despesas pessoais de pro-labore não entram no DRE da empresa

### Fluxo de caixa
```bash
curl -s -H "Authorization: Bearer $RECEITAS_MANAGER_TOKEN" \
  "$BASE_URL/api/nexus-manager?resource=fluxo-caixa&mes=2026-05&limit=100"
```

### Cheques
```bash
curl -s -H "Authorization: Bearer $RECEITAS_MANAGER_TOKEN" \
  "$BASE_URL/api/nexus-manager?resource=cheques&status=aberto&limit=100"
```
Status: `aberto`, `compensado`, `todas`

### Contas a pagar
```bash
curl -s -H "Authorization: Bearer $RECEITAS_MANAGER_TOKEN" \
  "$BASE_URL/api/nexus-manager?resource=contas-pagar&mes=2026-05&situacao=todas&limit=100"
```
Situação: `pago`, `aberto`, `cancelado`, `todas`

### Pro-labore
```bash
curl -s -H "Authorization: Bearer $RECEITAS_MANAGER_TOKEN" \
  "$BASE_URL/api/nexus-manager?resource=prolabore&mes=2026-05"
```
Filtro opcional: `&pessoa=Nome`

### Cartões
```bash
curl -s -H "Authorization: Bearer $RECEITAS_MANAGER_TOKEN" \
  "$BASE_URL/api/nexus-manager?resource=cartoes&mes=2026-05"
```

Para saldo atual dos cartões (preferir este endpoint):
```bash
curl -s -H "Authorization: Bearer $RECEITAS_MANAGER_TOKEN" \
  "$BASE_URL/api/nexus-manager?resource=saldo-cartoes"
```

### Pedidos de compra
```bash
curl -s -H "Authorization: Bearer $RECEITAS_MANAGER_TOKEN" \
  "$BASE_URL/api/nexus-manager?resource=pedidos-compra&mes=2026-05&limit=100"
```

### Resultado mensal (histórico)
```bash
curl -s -H "Authorization: Bearer $RECEITAS_MANAGER_TOKEN" \
  "$BASE_URL/api/nexus-manager?resource=resultado-mensal&limit=24"
```
Filtro opcional: `&mes=2026-05`

## Tratamento de respostas

- Para DRE: usar os campos `linhas`, `dre` e `regras` retornados por `resource=dre`
- Para saldo de cartões: usar `resource=saldo-cartoes` ou `saldos_atuais`
- Para listas grandes: resumir contagens, totais, datas e categorias
