import httpx
from app.core.config import settings

class LlmService:
    async def answer(self, message: str, context: str, language: str) -> str:
        if settings.model_provider != "ollama" and not settings.model_api_key:
            return context
        system = (
            "You are a B2B support chatbot for Indian users. Reply in the user's language "
            "(Hindi, English, Hinglish, or Indian native script). Use only the provided knowledge. "
            "If the knowledge does not answer the question, say so clearly."
        )
        payload = {
            "model": settings.model_chat_model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": f"Language: {language}\nKnowledge:\n{context}\n\nQuestion: {message}"}
            ],
            "temperature": 0.2
        }
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{settings.model_base_url.rstrip('/')}/chat/completions",
                headers={"Authorization": f"Bearer {settings.model_api_key}"},
                json=payload
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
