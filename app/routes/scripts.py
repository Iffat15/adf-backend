from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.script_service import save_script_to_db,list_scripts

router = APIRouter()

@router.post("/upload")
async def upload_script(script: UploadFile = File(...)):
    return await save_script_to_db(script)

@router.get("/all")
async def get_scripts():
    return await list_scripts()
