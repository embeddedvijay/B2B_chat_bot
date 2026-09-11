# B2B Chat Bot

Multi-tenant Indian-language support bot with MongoDB, common RAG chat, business-specific RAG sources, and future Windows CRM support. Docker is not required.

See [PROJECT_README.md](PROJECT_README.md) for architecture and [database/mongo-collections.md](database/mongo-collections.md) for configuration design.

## Local test

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python3 run_local.py
```

The test reads `rag-data/generic/*.txt` and `rag-data/businesses/<business_id>/*.txt`. Add your own plain TXT knowledge files there. `config/businesses.json` enables/disables business RAG, common RAG and general chat per business. Set `MODEL_API_KEY` in `.env` to get an actual multilingual AI response; without a key, the matching TXT content is returned so the RAG pipeline can be tested locally.
