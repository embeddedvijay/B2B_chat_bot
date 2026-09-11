from uuid import uuid4
from pathlib import Path
from app.core.config import settings
from app.rag.retrieval import TextFileRetriever
from app.schemas.chat import ChatMessageIn, ChatMessageOut
from app.services.language_service import LanguageService
from app.services.llm_service import LlmService
from app.services.business_config_service import BusinessConfigService

class ChatService:
    def __init__(self):
        self.language = LanguageService()
        rag_path = Path(__file__).resolve().parents[2] / settings.rag_data_path
        self.retriever = TextFileRetriever(str(rag_path))
        self.llm = LlmService()
        self.business_config = BusinessConfigService()

    async def reply(self, payload: ChatMessageIn) -> ChatMessageOut:
        language = self.language.detect(payload.message)
        config = self.business_config.get(payload.business_id)
        business_hits = await self.retriever.search_business(payload.business_id, payload.message) if config["business_rag_enabled"] else []
        if business_hits:
            context = "\n\n".join(hit["content"] for hit in business_hits)
            reply = await self.llm.answer(payload.message, context, language)
            return ChatMessageOut(conversation_id=payload.conversation_id or str(uuid4()), reply=reply, language=language, confidence=business_hits[0]["score"], handoff_required=False)
        common_hits = await self.retriever.search_common(payload.message) if config["common_rag_enabled"] else []
        if common_hits:
            context = "\n\n".join(hit["content"] for hit in common_hits)
            reply = await self.llm.answer(payload.message, context, language)
            return ChatMessageOut(conversation_id=payload.conversation_id or str(uuid4()), reply=reply, language=language, confidence=common_hits[0]["score"], handoff_required=False)
        if not config["general_chat_enabled"]:
            reply = "Is business ke liye general chat disabled hai. Main support ticket create kar sakta hoon." if language != "en" else "General chat is disabled for this business. I can create a support ticket."
            return ChatMessageOut(conversation_id=payload.conversation_id or str(uuid4()), reply=reply, language=language, confidence=0.0, handoff_required=True)
        # General chat is allowed only when business configuration enables it.
        reply = "Main iske liye general guidance de sakta hoon. Account, payment ya business-specific issue ke liye support ticket create karunga." if language != "en" else "I can provide general guidance. For account, payment, or business-specific issues, I will create a support ticket."
        return ChatMessageOut(conversation_id=payload.conversation_id or str(uuid4()), reply=reply, language=language, confidence=0.40, handoff_required=False)
