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
        hits = await self.retriever.search(payload.tenant_id, payload.message)
        if not hits:
            reply = "Mujhe approved knowledge base me iska confirmed answer nahi mila. Main support ticket create kar sakta hoon." if language != "en" else "I could not find a confirmed answer in the approved knowledge base. I can create a support ticket."
            return ChatMessageOut(conversation_id=payload.conversation_id or str(uuid4()), reply=reply, language=language, confidence=0.0, handoff_required=True)
        # Send only retrieved, tenant-scoped context to the configured LLM here.
        return ChatMessageOut(conversation_id=payload.conversation_id or str(uuid4()), reply="RAG response placeholder", language=language, confidence=0.85, handoff_required=False)
