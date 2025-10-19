
from fastapi import FastAPI, UploadFile, File,Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import subprocess
app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploaded_scripts")
print("UPLOAD_DIR:", UPLOAD_DIR)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# POST: Upload a script file
@app.post("/upload-script")
async def upload_script(script: UploadFile = File(...)):
    
    filename = script.filename

    # ✅ Check file extension
    if not filename.endswith(".py"):
        raise HTTPException(status_code=400, detail="Only .py files are allowed.")

    contents = await script.read()

    # ✅ Check if file is empty
    if not contents.strip():
        raise HTTPException(status_code=400, detail="Uploaded script is empty.")

    # Save the file
    with open(os.path.join(UPLOAD_DIR, filename), "wb") as f:
        f.write(contents)

    print(f"Received and saved: {filename}")
    return {"nodeLabel": filename}

# GET: List all uploaded scripts
@app.get("/scripts")
def list_scripts():
    try:
        files = os.listdir(UPLOAD_DIR)
        return {"scripts": files}
    except FileNotFoundError:
        return {"scripts": []}
    

# @app.get("/get-scripts")
# def get_uploaded_script_names():
#     try:
#         return [f for f in os.listdir(UPLOAD_DIR) if f.endswith(".py")]
#     except FileNotFoundError:
#         return []
    

# def run_uploaded_scripts_sequentially():
#     script_names = [f for f in os.listdir(UPLOAD_DIR) if f.endswith(".py")]
#     results = []

#     for script_name in script_names:
#         script_path = os.path.join(UPLOAD_DIR, script_name)
#         print(f"Running: {script_name}")

#         try:
#             result = subprocess.run(
#                 ["python", script_path],
#                 capture_output=True,
#                 text=True,
#                 check=False
#             )
#             results.append({
#                 "script": script_name,
#                 "stdout": result.stdout,
#                 "stderr": result.stderr,
#                 "returncode": result.returncode
#             })
#         except Exception as e:
#             results.append({
#                 "script": script_name,
#                 "error": str(e)
#             })

#     return results
# # UPLOAD_DIR = "uploaded_scripts"

# @app.get("/run-all-scripts")
# def run_all_scripts():
#     return {"results": run_uploaded_scripts_sequentially()}

@app.post("/run-pipeline")
async def run_pipeline(request: Request):
    try:
        data = await request.json()
        script_names = data.get("scripts", [])
    except Exception as e:
        return {"error": f"Invalid JSON body: {str(e)}"}

    results = []

    for script_name in script_names:
        script_path = os.path.join(UPLOAD_DIR, script_name)

        if not os.path.exists(script_path):
            results.append({
                "script": script_name,
                "error": "Script not found"
            })
            continue

        try:
            result = subprocess.run(
                ["python", script_path],
                capture_output=True,
                text=True,
                check=False  # prevents exception on non-zero exit
            )
            results.append({
                "script": script_name,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            })
        except Exception as e:
            results.append({
                "script": script_name,
                "error": str(e)
            })

    return {"results": results}