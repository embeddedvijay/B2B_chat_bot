# B2B Indic Support Bot

Multi-tenant RAG support platform for Indian businesses. It supports website/WhatsApp chat today and a Windows CRM desktop client later.

## Architecture

```text
Customer (web / WhatsApp / Windows CRM)
        -> FastAPI API
        -> tenant-safe RAG search + LLM response
        -> MongoDB Vector Search / Redis / object storage
        -> ticket + CRM / client APIs
```

## Modules

- `frontend-admin`: React admin dashboard for bot, documents, tickets and integrations.
- `backend`: FastAPI service. The only layer that accesses data, RAG, LLMs and customer CRM APIs.
- `windows-crm`: Electron/React shell for a future Windows agent CRM. It uses the same backend REST API; do not place RAG or database credentials in it.
- `database`: MongoDB collection design.
- `docs`: contracts and implementation notes.

## Main tenant rule

Every tenant-owned database query, document upload, vector search, ticket and conversation must carry `tenant_id`. This prevents company data leakage.

## Chat and RAG priority

1. Business RAG: enabled TXT files for the selected business.
2. Common RAG: shared answers for greetings, bot usage and common troubleshooting.
3. General chat: only when enabled in business config; it must not invent account, payment, policy or business data.
4. Fallback: create a ticket or transfer to a human for sensitive/low-confidence queries.

## Run backend locally

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

Open `http://127.0.0.1:8000/docs` for the initial API.

## Delivery roadmap

1. Admin login, tenant setup, document upload and indexing.
2. Web chat widget with Hindi, English and Hinglish responses.
3. Ticket/human handoff, source citations and feedback.
4. WhatsApp webhook and customer CRM/API tools.
5. Windows CRM agent desktop app using the endpoints in `docs/crm-api-contract.md`.
