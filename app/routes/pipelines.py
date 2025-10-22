# app/routes/pipelines.py
from fastapi import APIRouter, HTTPException, Body
from datetime import datetime
from bson import ObjectId
from typing import List
from app.db_config import db
from app.services.pipeline_service import run_pipeline  # your async runner
from app.services.pipeline_service import save_pipeline_to_db
router = APIRouter()

@router.post("/create-pipeline")
async def create_pipeline(
    name: str = Body(...),
    description: str = Body(...),
    nodes: list = Body(...),
    connections: list = Body(...)
):
    try:
        result = await save_pipeline_to_db(name, description, nodes, connections)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/save")
async def save_pipeline(payload: dict):
    """
    Save pipeline definition into db.pipelines.
    payload should include keys: name, nodes (list), connections (list), description (optional), sensitivity (optional)
    """
    name = payload.get("name")
    nodes = payload.get("nodes")
    connections = payload.get("connections", [])
    if not name or not nodes:
        raise HTTPException(status_code=400, detail="`name` and `nodes` are required")

    now = datetime.utcnow()
    doc = {
        "name": name,
        "description": payload.get("description", ""),
        "nodes": nodes,
        "connections": connections,
        "schedule": payload.get("schedule", {"cron": None, "enabled": False}),
        "sensitivity": payload.get("sensitivity", "low"),
        "tags": payload.get("tags", []),
        "created_by": payload.get("created_by", None),
        "created_at": now,
        "updated_at": now
    }

    res = await db.pipelines.insert_one(doc)
    return {"pipeline_id": str(res.inserted_id)}

@router.get("/")
async def list_pipelines():
    pipelines = []
    async for p in db.pipelines.find({}, {"name": 1, "description": 1, "created_at": 1, "sensitivity": 1}):
        pipelines.append({
            "pipeline_id": str(p["_id"]),
            "name": p.get("name"),
            "description": p.get("description"),
            "created_at": p.get("created_at"),
            "sensitivity": p.get("sensitivity")
        })
    return {"pipelines": pipelines}

@router.get("/{pipeline_id}")
async def get_pipeline(pipeline_id: str):
    try:
        obj_id = ObjectId(pipeline_id)  # Convert string to ObjectId
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid pipeline id: {e}")

    pipeline = await db.pipelines.find_one({"_id": obj_id})
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")

    # Convert ObjectId to string for JSON response
    pipeline["id"] = str(pipeline["_id"])
    del pipeline["_id"]  # optional
    return pipeline

@router.get("/run-pipeline/{pipeline_id}")
async def run_pipeline_api(pipeline_id: str):
    # Fetch pipeline from DB
    # pipeline = await db.pipelines.find_one({"_id": ObjectId(pipeline_id)})
    # if not pipeline:
    #     raise HTTPException(status_code=404, detail="Pipeline not found")

    # nodes = pipeline.get("nodes", [])

    # # Dummy execution logic using node_id
    # execution_order = [node["node_id"] for node in nodes]
    # results = {node["node_id"]: f"Executed {node['type']}" for node in nodes}

    # return {
    #     "execution_order": execution_order,
    #     "results": results
    # }
    try:
        result = await run_pipeline(pipeline_id)  # <- call the one from pipeline_service
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running pipeline: {str(e)}")
