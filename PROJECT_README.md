# B2B Indic Support Bot

Multi-tenant RAG support platform for Indian businesses. It supports website/WhatsApp chat today and a Windows CRM desktop client later.

## Architecture

```text
Customer (web / WhatsApp / Windows CRM)
        -> FastAPI API
        -> tenant-safe RAG search + LLM response
        -> PostgreSQL + pgvector / Redis / object storage
        -> ticket + CRM / client APIs
```

## Modules

- `frontend-admin`: React admin dashboard for bot, documents, tickets and integrations.
- `backend`: FastAPI service. The only layer that accesses data, RAG, LLMs and customer CRM APIs.
- `windows-crm`: Electron/React shell for a future Windows agent CRM. It uses the same backend REST API; do not place RAG or database credentials in it.
- `database`: PostgreSQL + pgvector starter schema.
- `docs`: contracts and implementation notes.

## Main tenant rule

Every tenant-owned database query, document upload, vector search, ticket and conversation must carry `tenant_id`. This prevents company data leakage.

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
