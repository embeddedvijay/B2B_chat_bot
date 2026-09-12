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

## Local model setup (no API payment)

Install Ollama on the same server, then download the default multilingual chat model once:

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5:3b
ollama serve
```

The default `.env.example` already points to Ollama at `http://127.0.0.1:11434/v1`; no paid API key is required. It uses `qwen2.5:3b`, selected for CPU-friendly multilingual support-chat testing. The test reads `rag-data/generic/*.txt` and `rag-data/businesses/<business_id>/*.txt`. Add your own plain TXT knowledge files there. `config/businesses.json` enables/disables business RAG, common RAG and general chat per business.

## Test the model directly

Before testing the project, verify that the local model responds correctly:

```bash
ollama run qwen2.5:3b
```

Hindi/Hinglish test:

```text
Hello, mera naam Vijay hai. Main Hindi aur Hinglish me baat karunga.
Mera login fail ho raha hai aur main frustrated hoon. Mere issue ko short me summarize karo.
```

Tamil test:

```text
வணக்கம், என் பெயர் விஜய். நான் தமிழில் பேச விரும்புகிறேன்.
எனது கணக்கில் உள்நுழைய முடியவில்லை. கடவுச்சொல்லை மாற்றினேன், ஆனால் மின்னஞ்சல் வரவில்லை.
நான் இதனால் மிகவும் கவலைப்படுகிறேன். தயவுசெய்து உதவுங்கள்.
என் பிரச்சினையை சுருக்கமாகச் சொல்லுங்கள்.
```

The model should reply in the selected language, retain the earlier messages in the same Ollama session, and respond empathetically to frustration.

## Project model configuration

`backend/.env` uses this local-only configuration:

```env
MODEL_PROVIDER=ollama
MODEL_BASE_URL=http://127.0.0.1:11434/v1
MODEL_CHAT_MODEL=qwen2.5:3b
MODEL_API_KEY=ollama
```

`MODEL_API_KEY=ollama` is a dummy local value. No paid API key is required.
