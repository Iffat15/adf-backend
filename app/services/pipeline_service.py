
import os
import json
import asyncio
from bson import ObjectId
from fastapi import HTTPException
from concurrent.futures import ThreadPoolExecutor
from app.db_config import db
from app.utils.io_utils import capture_stdout
from app.utils.temp_paths import TEMP_DIR
from datetime import datetime
from app.models.pipeline_model import PipelineModel
import copy

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
EXECUTION_LOG_FILE = os.path.join(PROJECT_ROOT, "execution_order.json")

# Ensure TEMP_DIR exists
os.makedirs(TEMP_DIR, exist_ok=True)

def execute_node(script_doc, prev_output_data):
    code = script_doc.get("code", "")
    name = script_doc.get("name", "unnamed_script.py")

    if not code.strip():
        raise Exception(f"Script {name} is empty")

    exec_globals = {"__name__": "__main__"}
    if prev_output_data:
        exec_globals["INPUT_DATA"] = prev_output_data

    current_output_path = os.path.join(TEMP_DIR, f"{ObjectId()}.json")
    exec_globals["OUTPUT_PATH"] = current_output_path

    print(f"[DEBUG] Executing {name} with INPUT_DATA = {prev_output_data}")  # <-- add this

    try:
        output_text = capture_stdout(code, exec_globals)
    except Exception as e:
        output_text = f"[ERROR] Node execution failed: {e}"

    node_output = None
    if os.path.exists(current_output_path):
        with open(current_output_path, "r") as f:
            try:
                node_output = json.load(f)
            except json.JSONDecodeError:
                node_output = None

    print(f"[EXECUTED] Node: {name}, Output Path: {current_output_path}")
    return {"node": name, "stdout": output_text, "output_data": node_output, "path": current_output_path}

def cleanup_temp_dir():
    for filename in os.listdir(TEMP_DIR):
        file_path = os.path.join(TEMP_DIR, filename)
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"[WARN] Failed to delete temp file {file_path}: {e}")

async def run_pipeline(pipeline_id: str):
    """
    1. This function executes a pipeline given its pipeline_id.
    2. It respects the DAG structure of the pipeline (Directed Acyclic Graph),
    i.e., nodes run only after their upstream dependencies finish.
    3. It supports parallel execution of nodes that can run independently.
    """
    
    """
    Step- 01 : Fetch the pipeline from MongoDB
    """
    pipeline = await db.pipelines.find_one({"_id": ObjectId(pipeline_id)})
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    """
    Step- 02 : Prepare nodes and edges
            1.nodes is a dictionary mapping each node _id to a simple object.
            2.edges is a list of connections, each of the form {"from": <node_id>, "to": <node_id>
    """
    # node_id -> node mapping
    nodes = {n: {"node_id": n} for n in pipeline.get("nodes", [])}
    edges = pipeline.get("connections", [])

    """
    Step 03 : Build dependency Graph
            1.graph → adjacency list for downstream nodes.
            2.indegree → number of upstream dependencies for each node.
            3.This allows us to find ready nodes (nodes with indegree=0) that can run immediately.
    """
    graph = {nid: [] for nid in nodes}       # node -> list of downstream nodes
    indegree = {nid: 0 for nid in nodes}    # node -> number of upstream dependencies
    for edge in edges:
        graph[edge["from"]].append(edge["to"]) # edge : u -> v, graph[u] = v, indegree[v]+=1
        indegree[edge["to"]] += 1
    """
    Step 04 : Initialize tracking structures
            1.output_data_map stores outputs of each node so downstream nodes can access it.
            2.execution_order helps for debugging/logging.
            3.results stores full execution results (like stdout, outputs, node info).
    """
    output_data_map = {}   # node_id -> output data
    execution_order = []
    results = []

    """
    Step 05 : Set up parallel execution
            1.A thread pool is used because Python scripts (execute_node) are usually CPU-bound or blocking.
            2.Asyncio can then schedule multiple nodes in parallel, but each node runs in its own thread
    """
    executor = ThreadPoolExecutor(max_workers=4)
    loop = asyncio.get_event_loop()

    """
    Step 06 : Identify initial ready nodes
            1.These are nodes with no upstream dependencies.
            2.They are the first to be executed.
    
    """
    ready_nodes = [nid for nid, deg in indegree.items() if deg == 0]

    print(f"[INFO] Starting pipeline: {pipeline['name']}")
    print(f"[INFO] TEMP_DIR: {TEMP_DIR}")


    """
    Step 07 : Main loop: execute ready nodes in parallel
    """
    while ready_nodes:
        tasks = []

        for node_id in ready_nodes:
            node = nodes[node_id]

            # Fetch script using node_id (node_id = script _id)
            """
            Step 08 : 
                    For each ready node:
                    Fetch its script from db.scripts.
                    Check if it exists.
            """
            script_doc = await db.scripts.find_one({"_id": ObjectId(node_id)})
            if not script_doc:
                raise HTTPException(status_code=400, detail=f"Missing script for node {node_id}")

            """
            Step 09 : Collect inputs from upstream nodes
                    1.For nodes with multiple upstream dependencies, all outputs are merged.
                    2.If outputs are lists, they are appended into merged_input["data"].
                    3.If outputs are dicts, they are merged directly.
            """
            prev_outputs = [
                output_data_map[src] for src, outs in graph.items() if node_id in outs and src in output_data_map
            ]
            
            # merged_input = {}
            # for out in prev_outputs:
            #     if not out:
            #         continue
            #     if isinstance(out, dict):
            #         merged_input.update(copy.deepcopy(out))
            #     elif isinstance(out, list):
            #         merged_input.setdefault("data", []).extend(copy.deepcopy(out))
            merged_input = {"data": []}
            for out in prev_outputs:
                if not out:
                    continue
                if isinstance(out, dict) and "data" in out:
                    merged_input["data"].extend(copy.deepcopy(out["data"]))
                elif isinstance(out, list):
                    merged_input["data"].extend(copy.deepcopy(out))

            """
            Step 10 : Schedule node execution
                        1.Each node is run in a thread from the ThreadPoolExecutor.
                        2.execute_node is a function that runs the Python script and returns its output
            """
            # Schedule node execution in thread pool
            tasks.append(loop.run_in_executor(executor, execute_node, script_doc, merged_input))
        """
        Step 11 : Wait for all tasks to complete
                    1.asyncio.gather waits for all parallel nodes to finish before moving on.
                    2.Ensures that dependent nodes only run after their upstream nodes are done.
        """
        # Wait for all ready nodes to complete
        node_results = await asyncio.gather(*tasks)

        """
        Step 12: Update results and dependencies
                    For Each completed node:
                        1.Stores output in output_data_map.
                        2.Marks its downstream nodes as having one less pending dependency.
        """
        # Update results and downstream dependencies
        for i, node_id in enumerate(ready_nodes):
            res = node_results[i]
            results.append(res)
            output_data_map[node_id] = res["output_data"]
            execution_order.append(node_id)

            print(f"[INFO] Node executed: {node_id} -> {res['node']}")

            for downstream in graph[node_id]:
                indegree[downstream] -= 1
        """
        Step 13 : Identify new ready nodes
                    1.Nodes whose all dependencies are satisfied are now ready to run.
                    2.The while ready_nodes loop continues until all nodes are executed.
        """
        # Identify new ready nodes (all dependencies satisfied)
        ready_nodes = [nid for nid, deg in indegree.items() if deg == 0 and nid not in output_data_map]

    # Cleanup temporary files
    cleanup_temp_dir()
    print(f"[INFO] Pipeline execution order: {execution_order}")

    return {
        "status": "✅ Pipeline executed successfully",
        "results": results,
        "execution_order": execution_order
    }


# Save pipeline to DB
async def save_pipeline_to_db(
    pipeline: PipelineModel
    ):
    pipeline_doc = {
        "name": pipeline.name,
        "description": pipeline.description or "",
        "nodes": pipeline.nodes,
        "connections": [conn.dict(by_alias=True) for conn in pipeline.connections],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    result = await db.pipelines.insert_one(pipeline_doc)
    return {
        "status": "✅ Pipeline saved successfully",
        "pipeline_id": str(result.inserted_id)}