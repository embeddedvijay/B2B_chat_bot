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

    async def answer(self, message: str, context: str, language: str, business_id: str) -> str:
        if business_id == "restaurant_crm":
            system = (
                "You are the virtual waiter and support assistant for a restaurant. Reply warmly in the "
                f"customer's language ({language}). Use only the provided restaurant knowledge. Be concise, "
                "helpful, and service-oriented. For greetings, welcome the customer and offer to show the menu, "
                "Today's Special, table booking, or order help. Never invent a restaurant name, menu item, price, "
                "stock quantity, order status, or payment result. For live availability, price, order, payment, "
                "or booking data, say you will check the restaurant system or ask staff."
            )
        else:
            system = (
                "You are a B2B support chatbot for Indian users. Reply in the user's language "
                "(Hindi, English, Hinglish, or Indian native script). Use only the provided knowledge. "
                "If the knowledge does not answer the question, say so clearly."
            )
        return await self._complete(
            system,
            f"Language: {language}\nKnowledge:\n{context}\n\nCustomer message: {message}"
        )

    async def general_answer(self, message: str, language: str, business_id: str) -> str:
        if business_id == "restaurant_crm":
            system = (
                "You are a friendly virtual waiter for a restaurant, replying in the customer's language "
                f"({language}). Greet warmly and keep replies short. For a greeting, say a natural welcome such "
                "as 'Namaste! Hamare restaurant me aapka swagat hai. Main menu, Today's Special, table booking "
                "ya order me help kar sakta hoon.' Do not invent restaurant name, menu items, prices, stock, "
                "order status, payment, or booking availability. For those live details, say you will check the "
                "restaurant system or connect staff."
            )
        else:
            system = (
                "You are a polite Indian-language B2B support chatbot. Reply in the user's language "
                f"({language}). Give short general help or greet the user. Do not invent business-specific "
                "facts. For live-data questions without verified knowledge, explain that you need to check "
                "the system or create a support ticket."
            )
        return await self._complete(system, message)
