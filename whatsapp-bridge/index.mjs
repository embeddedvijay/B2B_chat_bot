import "dotenv/config";
import makeWASocket, {
  DisconnectReason,
  fetchLatestBaileysVersion,
  makeCacheableSignalKeyStore,
  useMultiFileAuthState
} from "@whiskeysockets/baileys";
import pino from "pino";
import qrcode from "qrcode-terminal";

const BACKEND_URL = (process.env.BACKEND_URL || "http://127.0.0.1:8000").replace(/\/$/, "");
const BRIDGE_SECRET = process.env.BRIDGE_SECRET || "";
const TENANT_ID = process.env.TENANT_ID || "local";
const BUSINESS_ID = process.env.BUSINESS_ID || "default";
const AUTH_DIR = process.env.AUTH_DIR || "./auth_info";
const logger = pino({ level: process.env.LOG_LEVEL || "info" });

if (!BRIDGE_SECRET) {
  throw new Error("BRIDGE_SECRET is required. Copy .env.example to .env and set a long random value.");
}

function messageText(message) {
  return (
    message.conversation ||
    message.extendedTextMessage?.text ||
    message.imageMessage?.caption ||
    message.videoMessage?.caption ||
    ""
  ).trim();
}

function isIndividualChat(remoteJid) {
  return remoteJid.endsWith("@s.whatsapp.net") || remoteJid.endsWith("@lid");
}

async function askBot(message, remoteJid) {
  const customerId = remoteJid.replace(/@.*$/, "");
  const response = await fetch(`${BACKEND_URL}/api/channels/whatsapp/incoming`, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "x-bridge-secret": BRIDGE_SECRET
    },
    body: JSON.stringify({
      tenant_id: TENANT_ID,
      business_id: BUSINESS_ID,
      customer_id: customerId,
      conversation_id: `whatsapp:${customerId}`,
      message
    })
  });
  if (!response.ok) {
    throw new Error(`Backend returned ${response.status}: ${await response.text()}`);
  }
  return response.json();
}

async function start() {
  const { state, saveCreds } = await useMultiFileAuthState(AUTH_DIR);
  const { version } = await fetchLatestBaileysVersion();
  const socket = makeWASocket({
    version,
    auth: {
      creds: state.creds,
      keys: makeCacheableSignalKeyStore(state.keys, logger)
    },
    logger,
    printQRInTerminal: false,
    syncFullHistory: false,
    markOnlineOnConnect: false,
    generateHighQualityLinkPreview: false
  });

  socket.ev.on("creds.update", saveCreds);

  socket.ev.on("connection.update", ({ connection, lastDisconnect, qr }) => {
    if (qr) {
      console.log("\nScan this QR in WhatsApp: Linked devices > Link a device\n");
      qrcode.generate(qr, { small: true });
    }
    if (connection === "open") {
      console.log("WhatsApp connected. Bot is ready.");
    }
    if (connection === "close") {
      const statusCode = lastDisconnect?.error?.output?.statusCode;
      const loggedOut = statusCode === DisconnectReason.loggedOut;
      console.log(loggedOut ? "WhatsApp logged out. Delete auth_info and scan QR again." : "Connection closed. Reconnecting...");
      if (!loggedOut) start().catch((error) => logger.error(error, "Reconnect failed"));
    }
  });

  socket.ev.on("messages.upsert", async ({ messages, type }) => {
    if (type !== "notify" && type !== "append") return;
    console.log(`Received ${type} event with ${messages.length} message(s)`);
    for (const msg of messages) {
      const remoteJid = msg.key.remoteJid || "";
      if (msg.key.fromMe || remoteJid === "status@broadcast" || !isIndividualChat(remoteJid)) continue;
      const text = messageText(msg.message || {});
      if (!text) {
        console.log(`Ignoring non-text message from ${remoteJid}`);
        continue;
      }
      try {
        console.log(`Incoming WhatsApp message from ${remoteJid}: ${text}`);
        const result = await askBot(text, remoteJid);
        if (result.reply) {
          await socket.sendMessage(remoteJid, { text: result.reply }, { quoted: msg });
          console.log(`Bot reply sent to ${remoteJid}`);
        }
      } catch (error) {
        logger.error(error, "Unable to process WhatsApp message");
      }
    }
  });
}

start().catch((error) => {
  logger.error(error, "WhatsApp bridge failed to start");
  process.exit(1);
});
