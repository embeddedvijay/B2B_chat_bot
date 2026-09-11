from fastapi import APIRouter
from app.schemas.chat import ChatMessageIn, ChatMessageOut
from app.services.chat_service import ChatService

router = APIRouter()
service = ChatService()

@router.post("/message", response_model=ChatMessageOut)
async def send_message(payload: ChatMessageIn):
    return await service.reply(payload)
