from fastapi import FastAPI
import uvicorn
from app.api.router import api_router
from app.core.config import settings

app = FastAPI(title=settings.app_name, version="0.1.0")
app.include_router(api_router, prefix="/api")

@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.app_name}

def main():
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=True)

if __name__ == "__main__":
    main()
