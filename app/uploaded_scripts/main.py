
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from datetime import datetime
from bson import ObjectId
import io, contextlib, json, os

# MongoDB import
from db_config import db, test_connection

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploaded_scripts")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -------------------- Startup Event --------------------
@app.on_event("startup")
async def startup_db_check():
    await test_connection()


# -------------------- Upload Script --------------------
@app.post("/upload-script")
async def upload_script(script: UploadFile = File(...)):
    filename = script.filename

    if not filename.endswith(".py"):
        raise HTTPException(status_code=400, detail="Only .py files are allowed.")

    contents = await script.read()
    if not contents.strip():
        raise HTTPException(status_code=400, detail="Uploaded script is empty.")

    # Save file locally
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(contents)
    print(f"Saved locally: {filename}")

    # Save script to MongoDB
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
        print(f"Saved to MongoDB with id: {result.inserted_id}")
    except Exception as e:
        print("❌ Failed to save script to MongoDB:", e)
        raise HTTPException(status_code=500, detail="Failed to save script to MongoDB")

    return {"filename": filename, "mongo_id": str(result.inserted_id)}


# -------------------- Get Scripts --------------------
@app.get("/get-scripts")
async def get_scripts():
    try:
        scripts = []
        async for script in db.scripts.find({}, {"_id": 1, "name": 1, "created_at": 1}):
            scripts.append({
                "mongo_id": str(script["_id"]),
                "name": script["name"],
                "created_at": script.get("created_at")
            })
        return {"scripts": scripts}
    except Exception as e:
        print("❌ Failed to fetch scripts from MongoDB:", e)
        raise HTTPException(status_code=500, detail="Failed to fetch scripts from MongoDB")


from bson import ObjectId
import contextlib
import io


# -------------------- Run Script from DB --------------------

@app.get("/run-script/{script_id}")
async def run_script(script_id: str):
    """
    Fetch a script from MongoDB by ID and execute it.
    The script is executed in an isolated namespace, 
    and its stdout is captured and returned.
    """
    try:
        script_doc = await db.scripts.find_one({"_id": ObjectId(script_id)})
        if not script_doc:
            raise HTTPException(status_code=404, detail="Script not found in MongoDB")

        script_str = script_doc.get("code", "")
        if not script_str.strip():
            raise HTTPException(status_code=400, detail="Script content is empty")

        # Capture stdout
        stdout = io.StringIO()

        # Prepare globals so __name__ behaves like a real script
        exec_globals = {"__name__": "__main__"}

        with contextlib.redirect_stdout(stdout):
            try:
                exec(script_str, exec_globals)
                output = stdout.getvalue()
            except Exception as e:
                output = f"❌ Error executing script: {str(e)}"

        return {
            "script_id": script_id,
            "name": script_doc.get("name"),
            "output": output
        }

    except Exception as e:
        print("❌ Error while running script:", e)
        raise HTTPException(status_code=500, detail=f"Error while running script: {str(e)}")
    
#-------------------Run Pipeline---------------------

TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp_data")
os.makedirs(TEMP_DIR, exist_ok=True)


@app.post("/run-pipeline")
async def run_pipeline(node_ids: list[str]):
    """
    Runs multiple nodes in sequence.
    Each node's output file is passed to the next node as input.
    """
    try:
        prev_output_path = None
        results = []

        for node_id in node_ids:
            # Fetch script
            script_doc = await db.scripts.find_one({"_id": ObjectId(node_id)})
            if not script_doc:
                raise HTTPException(status_code=404, detail=f"Node {node_id} not found in DB")

            script_str = script_doc.get("code", "")
            script_name = script_doc.get("name", "unknown.py")
            if not script_str.strip():
                raise HTTPException(status_code=400, detail=f"Node {script_name} has empty script")

            # Prepare output redirection
            stdout = io.StringIO()
            exec_globals = {"__name__": "__main__"}

            # Set environment var for previous output (optional)
            if prev_output_path:
                exec_globals["PREV_OUTPUT_PATH"] = prev_output_path

            # Create a unique temp output file
            current_output_path = os.path.join(TEMP_DIR, f"{ObjectId()}.json")
            exec_globals["CURRENT_OUTPUT_PATH"] = current_output_path

            with contextlib.redirect_stdout(stdout):
                try:
                    exec(script_str, exec_globals)
                    output = stdout.getvalue()
                except Exception as e:
                    output = f"❌ Error in {script_name}: {str(e)}"

            results.append({
                "node": script_name,
                "output": output
            })

            prev_output_path = current_output_path  # Pass forward

        return {
            "status": "✅ Pipeline executed successfully",
            "results": results
        }

    except Exception as e:
        print("❌ Pipeline execution error:", e)
        raise HTTPException(status_code=500, detail=f"Pipeline execution failed: {str(e)}")
