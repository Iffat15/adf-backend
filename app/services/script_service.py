import os
from datetime import datetime
from fastapi import HTTPException
from bson import ObjectId
from app.db_config import db
from app.utils.io_utils import capture_stdout
from app.models.node_model import NodeModel
from app.db_config import db

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploaded_scripts")
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_script_to_db(node: NodeModel):
    
    result = await db["scripts"].insert_one(node.model_dump())
    return {"message": "Script uploaded successfully", "id": str(result.inserted_id)}

# async def list_scripts():
#     scripts = await db["scripts"].find().to_list(100)
#     return scripts
async def list_scripts():
    scripts = await db["scripts"].find().to_list(100)
    return [
        {**script, "_id": str(script["_id"])}  # ✅ Convert ObjectId to string
        for script in scripts
    ]

async def run_script_by_id(script_id: str):
    try:
        script_doc = await db.scripts.find_one({"_id": ObjectId(script_id)})
        if not script_doc:
            raise HTTPException(status_code=404, detail="Script not found")
        code = script_doc.get("code", "")
        if not code.strip():
            raise HTTPException(status_code=400, detail="Script content is empty")

        output = capture_stdout(code)
        return {
                "script_id": script_id, 
                "name": script_doc.get("name"),
                "type": script_doc.get("type", "unknown"),  # fallback just in case,
                "output": output}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while running script: {str(e)}")
