# WhatsApp Test Bridge

This is a local-only WhatsApp test connector for the B2B chatbot. It uses WhatsApp QR linking, then forwards one-to-one incoming text messages to the existing FastAPI bot and sends the generated reply back to the same WhatsApp chat.

It is intentionally separated from the chatbot core. When the future self-hosted chat app is ready, replace this bridge with a WebSocket/mobile adapter; the RAG and Ollama chatbot code remains the same.

## Run locally

Start the Python bot first:

```bash
cd backend
source .venv/bin/activate
cp .env.example .env
```

Set the same strong secret in both files:

```env
# backend/.env
WHATSAPP_BRIDGE_SECRET=use-a-long-random-secret

# whatsapp-bridge/.env
BRIDGE_SECRET=use-a-long-random-secret
```

Then start FastAPI:

```bash
python3 run_local.py
```

In a second terminal, install and run the connector:

```bash
cd whatsapp-bridge
cp .env.example .env
npm install
npm start
```

A QR code appears in the terminal. In the WhatsApp phone app open **Linked devices**, choose **Link a device**, and scan it. Send a text from another WhatsApp number to the linked number. The connector calls `POST /api/channels/whatsapp/incoming`, which reuses the existing RAG/Ollama ChatService and sends its reply back.

## Local data and safety

- `.env` and `auth_info/` are not committed. `auth_info/` contains the linked-device credentials.
- Only individual text chats are handled. Status, group, media-only, and self-sent messages are ignored.
- This is a WhatsApp Web-based test connector, not Meta's official Business API. Use a dedicated test number and do not use it for bulk or unsolicited messaging.
