from fastapi import APIRouter
from app.api import chat, documents, tickets, crm

api_router = APIRouter()
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
api_router.include_router(crm.router, prefix="/crm", tags=["windows-crm"])
