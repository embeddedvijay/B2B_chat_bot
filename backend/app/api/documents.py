from fastapi import APIRouter, UploadFile, File, Form

router = APIRouter()

@router.post("/upload")
async def upload_document(tenant_id: str = Form(...), file: UploadFile = File(...)):
    # Store in object storage, create document row, then queue indexing worker.
    return {"tenant_id": tenant_id, "filename": file.filename, "status": "queued_for_indexing"}
