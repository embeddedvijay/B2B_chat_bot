from uuid import uuid4
from app.rag.retrieval import TenantRetriever
from app.schemas.chat import ChatMessageIn, ChatMessageOut
from app.services.language_service import LanguageService

class ChatService:
    def __init__(self):
        self.language = LanguageService()
        self.retriever = TenantRetriever()

    async def reply(self, payload: ChatMessageIn) -> ChatMessageOut:
        language = self.language.detect(payload.message)
        business_hits = await self.retriever.search_business(payload.tenant_id, payload.message)
        if business_hits:
            return ChatMessageOut(conversation_id=payload.conversation_id or str(uuid4()), reply="Business RAG response placeholder", language=language, confidence=0.90, handoff_required=False)
        common_hits = await self.retriever.search_common(payload.message)
        if common_hits:
            return ChatMessageOut(conversation_id=payload.conversation_id or str(uuid4()), reply="Common RAG response placeholder", language=language, confidence=0.80, handoff_required=False)
        # General chat is allowed only when business configuration enables it.
        reply = "Main iske liye general guidance de sakta hoon. Account, payment ya business-specific issue ke liye support ticket create karunga." if language != "en" else "I can provide general guidance. For account, payment, or business-specific issues, I will create a support ticket."
        return ChatMessageOut(conversation_id=payload.conversation_id or str(uuid4()), reply=reply, language=language, confidence=0.40, handoff_required=False)
