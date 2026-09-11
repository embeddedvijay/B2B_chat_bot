from fastapi import APIRouter

router = APIRouter()

@router.get("/agent-queue")
async def agent_queue(tenant_id: str, agent_id: str):
    return {"tenant_id": tenant_id, "agent_id": agent_id, "conversations": []}

@router.get("/customers/{customer_id}/timeline")
async def customer_timeline(customer_id: str, tenant_id: str):
    return {"tenant_id": tenant_id, "customer_id": customer_id, "events": []}
