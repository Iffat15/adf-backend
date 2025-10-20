import os
from datetime import datetime
from fastapi import HTTPException
from bson import ObjectId
from app.db_config import db
from app.utils.io_utils import capture_stdout

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploaded_scripts")
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_script_to_db(script):
    filename = script.filename

    if not filename.endswith(".py"):
        raise HTTPException(status_code=400, detail="Only .py files are allowed.")

    contents = await script.read()
    if not contents.strip():
        raise HTTPException(status_code=400, detail="Uploaded script is empty.")

    # Save locally
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(contents)

    # Save to DB
    try:
        script_doc = {
            "name": filename,
            "description": f"Uploaded script: {filename}",
            "code": contents.decode("utf-8"),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "tags": ["uploaded"]
        }
        result = await db.scripts.insert_one(script_doc)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to save script to MongoDB")

    return {"filename": filename, "mongo_id": str(result.inserted_id)}

async def list_scripts():
    try:
        scripts = []
        async for script in db.scripts.find({}, {"_id": 1, "name": 1, "created_at": 1}):
            scripts.append({
                "mongo_id": str(script["_id"]),
                "name": script["name"],
                "created_at": script.get("created_at")
            })
        return {"scripts": scripts}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch scripts from MongoDB")

async def run_script_by_id(script_id: str):
    try:
        script_doc = await db.scripts.find_one({"_id": ObjectId(script_id)})
        if not script_doc:
            raise HTTPException(status_code=404, detail="Script not found")
        code = script_doc.get("code", "")
        if not code.strip():
            raise HTTPException(status_code=400, detail="Script content is empty")

        output = capture_stdout(code)
        return {"script_id": script_id, "name": script_doc.get("name"), "output": output}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while running script: {str(e)}")
