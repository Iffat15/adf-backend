from fastapi import APIRouter, HTTPException
from app.services.script_service import run_script_by_id
from app.services.pipeline_service import run_pipeline_nodes

router = APIRouter()

@router.get("/script/{script_id}")
async def run_script(script_id: str):
    return await run_script_by_id(script_id)

@router.post("/pipeline")
async def run_pipeline(node_ids: list[str]):
    return await run_pipeline_nodes(node_ids)
