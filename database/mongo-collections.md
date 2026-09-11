# MongoDB Collections

| Collection | Purpose |
| --- | --- |
| `businesses` | Business identity and branding |
| `business_configs` | Enabled RAG sources, languages, APIs and fallback policy |
| `rag_documents` | Uploaded TXT/PDF source metadata |
| `rag_chunks` | Text chunks, embeddings, `business_id`, `source_scope`, enabled state |
| `conversations`, `messages` | Customer and agent conversation history |
| `customers`, `tickets` | CRM support data |

## Example business configuration

```json
{
  "business_id": "restaurant_crm",
  "enabled": true,
  "languages": ["hi", "en", "hinglish"],
  "rag": {
    "business_sources_enabled": ["inventory"],
    "common_rag_enabled": true,
    "minimum_confidence": 0.72
  },
  "general_chat_enabled": true,
  "fallback_mode": "ticket"
}
```
