import secrets
from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel, Field
from app.core.config import settings
from app.schemas.chat import ChatMessageIn, ChatMessageOut
from app.services.chat_service import ChatService

router = APIRouter()
service = ChatService()

class WhatsAppIncoming(BaseModel):
    tenant_id: str = Field(min_length=1)
    business_id: str = Field(default="default", min_length=1)
    customer_id: str = Field(min_length=1)
    conversation_id: str = Field(min_length=1)
    message: str = Field(min_length=1, max_length=8000)

@router.post("/incoming", response_model=ChatMessageOut)
async def incoming_message(
    payload: WhatsAppIncoming,
    x_bridge_secret: str = Header(default="")
):
    if not settings.whatsapp_bridge_secret or not secrets.compare_digest(
        x_bridge_secret,
        settings.whatsapp_bridge_secret
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid WhatsApp bridge secret"
        )
    return await service.reply(ChatMessageIn(
        tenant_id=payload.tenant_id,
        business_id=payload.business_id,
        customer_id=payload.customer_id,
        conversation_id=payload.conversation_id,
        message=payload.message,
        channel="whatsapp"
    ))
