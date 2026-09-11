from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import settings

app = FastAPI(title=settings.app_name, version="0.1.0")
app.include_router(api_router, prefix="/api")

@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.app_name}
