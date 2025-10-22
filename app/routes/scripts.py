from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from datetime import datetime
from app.models.node_model import NodeModel
from app.services.script_service import save_script_to_db, list_scripts
from typing import List



router = APIRouter()

@router.post("/upload")
async def upload_script(
    script: UploadFile = File(...),
    node_type: str = Form(...)
):
    # Read script content
    content = await script.read()

    # Create NodeModel instance
    node = NodeModel(
        name=script.filename,
        type=node_type,
        description=f"Uploaded script: {script.filename}",
        code=content.decode("utf-8"),  # convert bytes to string
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Pass the NodeModel to your service to save
    return await save_script_to_db(node)

@router.get("/all", response_model=List[NodeModel])
async def get_scripts():
    return await list_scripts()
