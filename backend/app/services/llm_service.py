import httpx
from app.core.config import settings

class LlmService:
    async def _complete(self, system: str, user: str) -> str:
        payload = {
            "model": settings.model_chat_model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user}
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

    async def answer(self, message: str, context: str, language: str) -> str:
        if settings.model_provider != "ollama" and not settings.model_api_key:
            return context
        system = (
            "You are a B2B support chatbot for Indian users. Reply in the user's language "
            "(Hindi, English, Hinglish, or Indian native script). Use only the provided knowledge. "
            "If the knowledge does not answer the question, say so clearly."
        )
        return await self._complete(
            system,
            f"Language: {language}\nKnowledge:\n{context}\n\nQuestion: {message}"
        )

    async def general_answer(self, message: str, language: str) -> str:
        system = (
            "You are a polite Indian-language B2B support chatbot. Reply in the user's language "
            f"({language}). Give short general help or greet the user. Do not invent restaurant "
            "menu items, prices, inventory, order status, payments, bookings, or account data. "
            "For any business-specific or live-data question without verified knowledge, explain "
            "that you need to check the system or create a support ticket."
        )
        return await self._complete(system, message)
