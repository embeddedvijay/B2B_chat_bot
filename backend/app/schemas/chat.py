from pydantic import BaseModel, Field

class ChatMessageIn(BaseModel):
    tenant_id: str = Field(min_length=1)
    business_id: str = Field(default="default", min_length=1)
    customer_id: str | None = None
    conversation_id: str | None = None
    message: str = Field(min_length=1, max_length=8000)
    channel: str = "web"

class Source(BaseModel):
    document_id: str
    title: str
    score: float

class ChatMessageOut(BaseModel):
    conversation_id: str
    reply: str
    language: str
    confidence: float
    handoff_required: bool
    sources: list[Source] = []
