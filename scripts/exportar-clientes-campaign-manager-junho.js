#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const BASE_URL = (process.env.CAMPAIGN_MANAGER_URL || "").replace(/\/+$/, "");
const TOKEN = process.env.CAMPAIGN_MANAGER_TOKEN || "";

const START = new Date("2026-06-01T00:00:00.000-03:00");
const END = new Date("2026-07-01T00:00:00.000-03:00");

const OUT = path.resolve(
  __dirname,
  "../saidas/clientes-campaign-manager-2026-06-01-a-2026-06-30.csv"
);

if (!BASE_URL || !TOKEN) {
  console.error("Faltam CAMPAIGN_MANAGER_URL ou CAMPAIGN_MANAGER_TOKEN no ambiente.");
  process.exit(1);
}

async function api(pathname) {
  const response = await fetch(`${BASE_URL}${pathname}`, {
    headers: {
      Authorization: `Bearer ${TOKEN}`,
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    throw new Error(`${pathname}: HTTP ${response.status}`);
  }

  return response.json();
}

function csvCell(value) {
  const text = value == null ? "" : String(value);
  return `"${text.replace(/"/g, '""')}"`;
}

function labelTitles(labels) {
  return (labels || []).map((label) => label.title).filter(Boolean);
}

function keyFor(conversation) {
  return conversation.customerPhone || conversation.externalChatId || conversation.id;
}

function betterName(current, candidate) {
  if (!current) return candidate || "";
  if (!candidate) return current;
  return candidate.length > current.length ? candidate : current;
}

async function mapLimit(items, limit, worker) {
  const results = new Array(items.length);
  let next = 0;

  async function run() {
    while (next < items.length) {
      const index = next++;
      results[index] = await worker(items[index], index);
    }
  }

  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, run));
  return results;
}

async function main() {
  const [active, archived] = await Promise.all([
    api("/api/conversations?view=active&search=&channelId="),
    api("/api/conversations?view=archived&search=&channelId="),
  ]);

  const conversations = [
    ...(active.conversations || []),
    ...(archived.conversations || []),
  ];

  const candidates = conversations.filter((conversation) => {
    if (!conversation.lastActivity) return true;
    return new Date(conversation.lastActivity) >= START;
  });

  const rowsByClient = new Map();
  let conversationsWithInbound = 0;
  let inboundMessages = 0;

  await mapLimit(candidates, 8, async (conversation) => {
    const data = await api(`/api/conversations/${conversation.id}/messages`);
    const messages = data.messages || [];
    const inboundInPeriod = messages.filter((message) => {
      if (message.direction !== "in" || !message.occurredAt) return false;
      const occurredAt = new Date(message.occurredAt);
      return occurredAt >= START && occurredAt < END;
    });

    if (inboundInPeriod.length === 0) return;

    conversationsWithInbound += 1;
    inboundMessages += inboundInPeriod.length;

    inboundInPeriod.sort((a, b) => new Date(a.occurredAt) - new Date(b.occurredAt));

    const key = keyFor(conversation);
    const existing = rowsByClient.get(key);
    const firstInboundAt = inboundInPeriod[0].occurredAt;
    const lastInboundAt = inboundInPeriod[inboundInPeriod.length - 1].occurredAt;
    const labels = labelTitles(conversation.labels);

    if (!existing) {
      rowsByClient.set(key, {
        nome: conversation.customerName || inboundInPeriod[0].senderName || "",
        telefone: conversation.customerPhone || inboundInPeriod[0].senderPhone || "",
        canais: new Set([conversation.channelName].filter(Boolean)),
        primeiraMensagemCliente: firstInboundAt,
        ultimaMensagemCliente: lastInboundAt,
        mensagensClienteNoPeriodo: inboundInPeriod.length,
        conversasComContatoNoPeriodo: 1,
        statusConversas: new Set([conversation.status].filter(Boolean)),
        arquivada: conversation.archived ? "sim" : "nao",
        etiquetas: new Set(labels),
        rotulosOperacionais: new Set([conversation.operationalLabel].filter(Boolean)),
        retornante: conversation.isReturning ? "sim" : "nao",
        conversationIds: new Set([conversation.id]),
      });
      return;
    }

    existing.nome = betterName(existing.nome, conversation.customerName || inboundInPeriod[0].senderName);
    existing.telefone = existing.telefone || conversation.customerPhone || inboundInPeriod[0].senderPhone || "";
    if (conversation.channelName) existing.canais.add(conversation.channelName);
    if (new Date(firstInboundAt) < new Date(existing.primeiraMensagemCliente)) {
      existing.primeiraMensagemCliente = firstInboundAt;
    }
    if (new Date(lastInboundAt) > new Date(existing.ultimaMensagemCliente)) {
      existing.ultimaMensagemCliente = lastInboundAt;
    }
    existing.mensagensClienteNoPeriodo += inboundInPeriod.length;
    existing.conversasComContatoNoPeriodo += 1;
    if (conversation.status) existing.statusConversas.add(conversation.status);
    existing.arquivada = existing.arquivada === "sim" && conversation.archived ? "sim" : "parcial/nao";
    for (const label of labels) existing.etiquetas.add(label);
    if (conversation.operationalLabel) existing.rotulosOperacionais.add(conversation.operationalLabel);
    if (conversation.isReturning) existing.retornante = "sim";
    existing.conversationIds.add(conversation.id);
  });

  const header = [
    "nome",
    "telefone",
    "canais",
    "primeira_mensagem_cliente_no_periodo",
    "ultima_mensagem_cliente_no_periodo",
    "mensagens_cliente_no_periodo",
    "conversas_com_contato_no_periodo",
    "status_conversas",
    "arquivada",
    "etiquetas",
    "rotulos_operacionais",
    "retornante",
    "conversation_ids",
  ];

  const rows = [...rowsByClient.values()].sort(
    (a, b) => new Date(a.primeiraMensagemCliente) - new Date(b.primeiraMensagemCliente)
  );

  const lines = [
    header.join(","),
    ...rows.map((row) =>
      [
        row.nome,
        row.telefone,
        [...row.canais].join(" | "),
        row.primeiraMensagemCliente,
        row.ultimaMensagemCliente,
        row.mensagensClienteNoPeriodo,
        row.conversasComContatoNoPeriodo,
        [...row.statusConversas].join(" | "),
        row.arquivada,
        [...row.etiquetas].join(" | "),
        [...row.rotulosOperacionais].join(" | "),
        row.retornante,
        [...row.conversationIds].join(" | "),
      ].map(csvCell).join(",")
    ),
  ];

  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT, `${lines.join("\n")}\n`);

  console.log(JSON.stringify({
    output: OUT,
    clients: rows.length,
    conversationsWithInbound,
    inboundMessages,
    candidateConversations: candidates.length,
    totalConversations: conversations.length,
  }, null, 2));
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
