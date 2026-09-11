import asyncio
import os
from app.schemas.chat import ChatMessageIn
from app.services.chat_service import ChatService

async def main():
    service = ChatService()
    print("Indian multilingual chatbot local test. Type exit to stop.")
    while True:
        message = input("You: ").strip()
        if message.lower() in {"exit", "quit"}:
            return
        business_id = os.getenv("BUSINESS_ID", "restaurant_crm")
        response = await service.reply(ChatMessageIn(tenant_id="local_test", business_id=business_id, message=message))
        print(f"Bot ({response.language}): {response.reply}\n")

if __name__ == "__main__":
    asyncio.run(main())
