from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def list_tickets(tenant_id: str):
    return {"tenant_id": tenant_id, "items": []}
