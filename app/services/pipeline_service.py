# import os
# from bson import ObjectId
# from fastapi import HTTPException
# from app.db_config import db
# from app.utils.io_utils import capture_stdout
# from app.utils.temp_paths import TEMP_DIR
# import io, contextlib

# current_output_path = os.path.join(TEMP_DIR, f"{ObjectId()}.json")
# print(current_output_path)
# async def run_pipeline_nodes(node_ids: list[str]):
#     prev_output_path = None
#     results = []

#     for node_id in node_ids:
#         node_doc = await db.scripts.find_one({"_id": ObjectId(node_id)})
#         if not node_doc:
#             raise HTTPException(status_code=404, detail=f"Node {node_id} not found")
#         code = node_doc.get("code", "")
#         name = node_doc.get("name", "unknown.py")
#         if not code.strip():
#             raise HTTPException(status_code=400, detail=f"Node {name} has empty script")

#         exec_globals = {"__name__": "__main__"}
#         if prev_output_path:
#             exec_globals["PREV_OUTPUT_PATH"] = prev_output_path
#         current_output_path = os.path.join(TEMP_DIR, f"{ObjectId()}.json")
#         exec_globals["CURRENT_OUTPUT_PATH"] = current_output_path

#         output = capture_stdout(code, exec_globals)
#         results.append({"node": name, "output": output})
#         prev_output_path = current_output_path

#     return {"status": "✅ Pipeline executed successfully", "results": results}
import json
# import tempfile
import os
from bson import ObjectId
from fastapi import HTTPException
from app.db_config import db
from app.utils.io_utils import capture_stdout
from app.utils.temp_paths import TEMP_DIR


async def run_pipeline_nodes(node_ids: list[str]):
    """
    Executes a list of scripts (nodes) stored in MongoDB in sequence.
    Each node’s output is passed as input to the next node.
    Temp files are managed by the backend and cleaned up automatically.
    """
    results = []
    prev_output_data = None

    print(f"[INFO] Using TEMP_DIR: {TEMP_DIR}")

    for node_id in node_ids:
        node_doc = await db.scripts.find_one({"_id": ObjectId(node_id)})
        if not node_doc:
            raise HTTPException(status_code=404, detail=f"Node {node_id} not found")

        code = node_doc.get("code", "")
        name = node_doc.get("name", f"script_{node_id}.py")
        if not code.strip():
            raise HTTPException(status_code=400, detail=f"Node {name} has empty script")

        # Prepare execution context
        exec_globals = {"__name__": "__main__"}

        # If previous node has output, pass it as JSON string
        if prev_output_data is not None:
            exec_globals["INPUT_DATA"] = prev_output_data

        # Create a unique temp output path for this node
        current_output_path = os.path.join(TEMP_DIR, f"{ObjectId()}.json")
        exec_globals["OUTPUT_PATH"] = current_output_path

        # Run the node script and capture its stdout
        output_text = capture_stdout(code, exec_globals)
        results.append({"node": name, "stdout": output_text})

        # Read the node’s generated output (if any)
        if os.path.exists(current_output_path):
            with open(current_output_path, "r") as f:
                try:
                    prev_output_data = json.load(f)
                except json.JSONDecodeError:
                    prev_output_data = None
        else:
            prev_output_data = None

    # ✅ Cleanup temporary files after execution
    cleanup_temp_dir()

    return {"status": "✅ Pipeline executed successfully", "results": results}


def cleanup_temp_dir():
    """
    Deletes all temp files created during pipeline execution.
    """
    for filename in os.listdir(TEMP_DIR):
        file_path = os.path.join(TEMP_DIR, filename)
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"[WARN] Failed to delete temp file {file_path}: {e}")
