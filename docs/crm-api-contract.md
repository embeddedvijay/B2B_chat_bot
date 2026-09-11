# Windows CRM API Contract

The Windows app is an authenticated agent client. It never calls the LLM provider, pgvector, Redis or database directly.

| Feature | API |
| --- | --- |
| Agent inbox | `GET /api/crm/agent-queue?tenant_id=&agent_id=` |
| Customer context | `GET /api/crm/customers/{customer_id}/timeline?tenant_id=` |
| Send message | `POST /api/chat/message` |
| List tickets | `GET /api/tickets?tenant_id=` |
| Upload knowledge | `POST /api/documents/upload` |

All requests use `Authorization: Bearer <access_token>`. The backend derives/validates `tenant_id` from the token in production; it is explicit only in this initial scaffold to make the data boundary visible.
