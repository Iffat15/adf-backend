from fastapi import APIRouter, HTTPException
from app.services.script_service import run_script_by_id
# from app.services.pipeline_service import run_pipeline_nodes
from fastapi import APIRouter, Body
# from app.services.pipeline_service import save_pipeline_to_db


router = APIRouter()



@router.get("/script/{script_id}")
async def run_script(script_id: str):
    return await run_script_by_id(script_id)
