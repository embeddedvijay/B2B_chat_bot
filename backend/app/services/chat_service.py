import logging
import re
from uuid import uuid4
from pathlib import Path
from app.core.config import settings
from app.rag.retrieval import TextFileRetriever
from app.schemas.chat import ChatMessageIn, ChatMessageOut
from app.services.language_service import LanguageService
from app.services.llm_service import LlmService
from app.services.business_config_service import BusinessConfigService

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        self.language = LanguageService()
        rag_path = Path(__file__).resolve().parents[2] / settings.rag_data_path
        self.retriever = TextFileRetriever(str(rag_path))
        self.llm = LlmService()
        self.business_config = BusinessConfigService()

    def _greeting_response(self, business_id: str, message: str) -> str | None:
        if business_id != "restaurant_crm":
            return None
        normalized = re.sub(r"[^a-zA-Z\s]", "", message).strip().lower()
        if normalized not in {"hi", "hello", "hey", "namaste", "hello ji", "hi ji"}:
            return None
        source = self.retriever.get_business_document(business_id, "greeting.txt")
        if not source:
            return None
        match = re.search(r"^RESPONSE:\s*(.+)$", source, flags=re.MULTILINE)
        if not match:
            return None
        logger.info("RAG direct response selected: businesses/%s/greeting.txt", business_id)
        return match.group(1).strip()

    async def reply(self, payload: ChatMessageIn) -> ChatMessageOut:
        language = self.language.detect(payload.message)
        config = self.business_config.get(payload.business_id)
        greeting = self._greeting_response(payload.business_id, payload.message)
        if greeting:
            return ChatMessageOut(conversation_id=payload.conversation_id or str(uuid4()), reply=greeting, language=language, confidence=1.0, handoff_required=False)
        business_hits = await self.retriever.search_business(payload.business_id, payload.message) if config["business_rag_enabled"] else []
        if business_hits:
            logger.info("RAG business sources selected: %s", [hit["source_file"] for hit in business_hits])
            context = "\n\n".join(hit["content"] for hit in business_hits)
            reply = await self.llm.answer(payload.message, context, language, payload.business_id)
            return ChatMessageOut(conversation_id=payload.conversation_id or str(uuid4()), reply=reply, language=language, confidence=business_hits[0]["score"], handoff_required=False)
        common_hits = await self.retriever.search_common(payload.message) if config["common_rag_enabled"] else []
        if common_hits:
            logger.info("RAG common sources selected: %s", [hit["source_file"] for hit in common_hits])
            context = "\n\n".join(hit["content"] for hit in common_hits)
            reply = await self.llm.answer(payload.message, context, language, payload.business_id)
            return ChatMessageOut(conversation_id=payload.conversation_id or str(uuid4()), reply=reply, language=language, confidence=common_hits[0]["score"], handoff_required=False)
        if not config["general_chat_enabled"]:
            reply = "Is business ke liye general chat disabled hai. Main support ticket create kar sakta hoon." if language != "en" else "General chat is disabled for this business. I can create a support ticket."
            return ChatMessageOut(conversation_id=payload.conversation_id or str(uuid4()), reply=reply, language=language, confidence=0.0, handoff_required=True)
        reply = await self.llm.general_answer(payload.message, language, payload.business_id)
        return ChatMessageOut(conversation_id=payload.conversation_id or str(uuid4()), reply=reply, language=language, confidence=0.20, handoff_required=False)
