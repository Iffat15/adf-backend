
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

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
EXECUTION_LOG_FILE = os.path.join(PROJECT_ROOT, "execution_order.json")

# Ensure TEMP_DIR exists
os.makedirs(TEMP_DIR, exist_ok=True)

# def save_execution_order(order_list):
#     with open(EXECUTION_LOG_FILE, "w") as f:
#         json.dump(order_list, f, indent=2)
#     print(f"[INFO] Execution order saved to {EXECUTION_LOG_FILE}")

# def execute_node(script_doc, prev_output_data):
#     """
#     Executes a single node script with optional input data.
#     """
#     code = script_doc.get("code", "")
#     name = script_doc.get("name", "unnamed_script.py")

#     if not code.strip():
#         raise Exception(f"Script {name} is empty")

#     exec_globals = {"__name__": "__main__"}
#     if prev_output_data:
#         exec_globals["INPUT_DATA"] = prev_output_data

#     current_output_path = os.path.join(TEMP_DIR, f"{ObjectId()}.json")
#     exec_globals["OUTPUT_PATH"] = current_output_path

#     try:
#         output_text = capture_stdout(code, exec_globals)
#     except Exception as e:
#         output_text = f"[ERROR] Node execution failed: {e}"

#     node_output = None
#     if os.path.exists(current_output_path):
#         with open(current_output_path, "r") as f:
#             try:
#                 node_output = json.load(f)
#             except json.JSONDecodeError:
#                 node_output = None

#     print(f"[EXECUTED] Node: {name}, Output Path: {current_output_path}")
#     return {"node": name, "stdout": output_text, "output_data": node_output, "path": current_output_path}
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

# async def run_pipeline(pipeline_id: str):
#     """
#     Executes a saved pipeline from the database with DAG-based parallelism.
#     Tracks execution order and ensures all nodes, including 'load', run.
#     """
#     pipeline = await db.pipelines.find_one({"_id": ObjectId(pipeline_id)})
#     if not pipeline:
#         raise HTTPException(status_code=404, detail="Pipeline not found")

#     nodes = {n["node_id"]: n for n in pipeline["nodes"]}
#     edges = pipeline.get("connections", [])

#     # Build dependency graph
#     graph = {nid: [] for nid in nodes}
#     indegree = {nid: 0 for nid in nodes}
#     for edge in edges:
#         graph[edge["from"]].append(edge["to"])
#         indegree[edge["to"]] += 1

#     output_data_map = {}
#     results = []
#     execution_order = []

#     executor = ThreadPoolExecutor(max_workers=4)
#     loop = asyncio.get_event_loop()

#     # Start with nodes with no dependencies (indegree == 0)
#     ready_nodes = [nid for nid, deg in indegree.items() if deg == 0]

#     print(f"[INFO] Starting pipeline: {pipeline['name']}")
#     print(f"[INFO] TEMP_DIR: {TEMP_DIR}")

#     while ready_nodes:
#         tasks = []
#         for node_id in ready_nodes:
#             node = nodes[node_id]
#             script_doc = await db.scripts.find_one({"_id": ObjectId(node["script_id"])})
#             if not script_doc:
#                 raise HTTPException(status_code=404, detail=f"Script for {node_id} not found")

#             # Merge outputs from all dependencies
#             prev_outputs = [
#                 output_data_map[src] for src, outs in graph.items() if node_id in outs and src in output_data_map
#             ]
#             merged_input = {}
#             for out in prev_outputs:
#                 if out:
#                     merged_input.update(out)

#             tasks.append(loop.run_in_executor(executor, execute_node, script_doc, merged_input))

#         node_results = await asyncio.gather(*tasks)

#         for i, node_id in enumerate(ready_nodes):
#             res = node_results[i]
#             results.append(res)
#             output_data_map[node_id] = res["output_data"]
#             execution_order.append(node_id)

#             print(f"[INFO] Node executed: {node_id} -> {res['node']}")

#             # Reduce indegree of downstream nodes
#             for nxt in graph[node_id]:
#                 indegree[nxt] -= 1

#         # Identify new ready nodes (all dependencies satisfied)
#         ready_nodes = [nid for nid, deg in indegree.items() if deg == 0 and nid not in output_data_map]

#     # Save execution order and cleanup
#     # save_execution_order(execution_order)
#     cleanup_temp_dir()

#     print(f"[INFO] Pipeline execution order: {execution_order}")
#     return {"status": "✅ Pipeline executed successfully", "results": results, "execution_order": execution_order}
from fastapi import HTTPException
from bson import ObjectId
from concurrent.futures import ThreadPoolExecutor
import asyncio

# async def run_pipeline(pipeline_id: str):
#     """
#     Executes a saved pipeline from the database with DAG-based parallelism.
#     Automatically starts nodes with no incoming dependencies,
#     ensuring even 'transform' or 'load' can begin if unconnected.
#     """
#     pipeline = await db.pipelines.find_one({"_id": ObjectId(pipeline_id)})
#     if not pipeline:
#         raise HTTPException(status_code=404, detail="Pipeline not found")

#     # ✅ Use node_id (your schema uses this)
#     nodes = {n["node_id"]: n for n in pipeline.get("nodes", [])}
#     edges = pipeline.get("connections", [])

#     # ✅ Build dependency graph safely
#     graph = {nid: [] for nid in nodes}
#     indegree = {nid: 0 for nid in nodes}
#     for edge in edges:
#         src = edge.get("from")
#         dst = edge.get("to")
#         if src in graph and dst in graph:
#             graph[src].append(dst)
#             indegree[dst] += 1

#     output_data_map = {}
#     results = []
#     execution_order = []

#     executor = ThreadPoolExecutor(max_workers=4)
#     loop = asyncio.get_event_loop()

#     # ✅ Start with nodes that have no dependencies
#     ready_nodes = [nid for nid, deg in indegree.items() if deg == 0]

#     # ✅ Fallback: if no indegree==0 nodes (cyclic or disconnected pipeline)
#     if not ready_nodes:
#         print("[WARN] No starting nodes found — assuming all are independent.")
#         ready_nodes = list(nodes.keys())

#     print(f"[INFO] Starting pipeline: {pipeline['name']}")
#     print(f"[INFO] TEMP_DIR: {TEMP_DIR}")

#     visited = set()

#     while ready_nodes:
#         tasks = []
#         for node_id in ready_nodes:
#             node = nodes[node_id]
#             visited.add(node_id)

#             script_id = node.get("script_id")
#             if not script_id:
#                 raise HTTPException(status_code=400, detail=f"Missing script_id for node {node_id}")

#             script_doc = await db.scripts.find_one({"_id": ObjectId(script_id)})
#             if not script_doc:
#                 raise HTTPException(status_code=404, detail=f"Script for node {node_id} not found")

#             # ✅ Collect outputs from all dependencies
#             prev_outputs = [
#                 output_data_map[src]
#                 for src, outs in graph.items()
#                 if node_id in outs and src in output_data_map
#             ]
#             merged_input = {}
#             for out in prev_outputs:
#                 merged_input.update(out or {})

#             # Execute node (in parallel)
#             tasks.append(loop.run_in_executor(executor, execute_node, script_doc, merged_input))

#         node_results = await asyncio.gather(*tasks)

#         for i, node_id in enumerate(ready_nodes):
#             res = node_results[i]
#             results.append(res)
#             output_data_map[node_id] = res.get("output_data", {})
#             execution_order.append(node_id)

#             print(f"[INFO] Node executed: {node_id} -> {res.get('node')}")

#             # ✅ Decrease indegree for downstream nodes
#             for nxt in graph.get(node_id, []):
#                 indegree[nxt] -= 1

#         # ✅ Find new nodes whose dependencies are now satisfied
#         ready_nodes = [
#             nid for nid, deg in indegree.items()
#             if deg == 0 and nid not in visited
#         ]

#     cleanup_temp_dir()

#     print(f"[INFO] Pipeline execution order: {execution_order}")
#     return {
#         "status": "✅ Pipeline executed successfully",
#         "results": results,
#         "execution_order": execution_order
#     }
# async def run_pipeline(pipeline_id: str):
#     """
#     Executes a saved pipeline with DAG-based parallelism.
#     Respects dependencies and runs nodes in the correct order.
#     """
#     pipeline = await db.pipelines.find_one({"_id": ObjectId(pipeline_id)})
#     if not pipeline:
#         raise HTTPException(status_code=404, detail="Pipeline not found")

#     # node_id -> node mapping
#     # nodes = {n["node_id"]: n for n in pipeline.get("nodes", [])}
#     # edges = pipeline.get("connections", [])
#     # node_id -> node mapping
#     nodes = {n: {"node_id": n} for n in pipeline.get("nodes", [])}
#     edges = pipeline.get("connections", [])

#     # Build dependency graph
#     graph = {nid: [] for nid in nodes}       # node -> list of downstream nodes
#     indegree = {nid: 0 for nid in nodes}    # node -> number of upstream dependencies

#     for edge in edges:
#         graph[edge["from"]].append(edge["to"])
#         indegree[edge["to"]] += 1

#     output_data_map = {}   # node_id -> output data
#     execution_order = []
#     results = []

#     executor = ThreadPoolExecutor(max_workers=4)
#     loop = asyncio.get_event_loop()

#     # Nodes with no dependencies
#     ready_nodes = [nid for nid, deg in indegree.items() if deg == 0]

#     print(f"[INFO] Starting pipeline: {pipeline['name']}")
#     print(f"[INFO] TEMP_DIR: {TEMP_DIR}")

#     while ready_nodes:
#         tasks = []

#         for node_id in ready_nodes:
#             node = nodes[node_id]

#             # Fetch script using node_id (node_id = script _id)
#             script_doc = await db.scripts.find_one({"_id": ObjectId(node_id)})
#             if not script_doc:
#                 raise HTTPException(status_code=400, detail=f"Missing script for node {node_id}")

#             # Merge outputs from all dependencies
#             prev_outputs = [
#                 output_data_map[src] for src, outs in graph.items() if node_id in outs and src in output_data_map
#             ]
#             merged_input = {}
#             # for out in prev_outputs:
#             #     if out:
#             #         merged_input.update(out)
#             for out in prev_outputs:
#                 if not out:
#                     continue
#                 if isinstance(out, dict):
#                     merged_input.update(out)
#                 elif isinstance(out, list):
#                     merged_input.setdefault("data", []).extend(out)

#             # Schedule node execution in thread pool
#             tasks.append(loop.run_in_executor(executor, execute_node, script_doc, merged_input))

#         # Wait for all ready nodes to complete
#         node_results = await asyncio.gather(*tasks)

#         # Update results and indegree
#         for i, node_id in enumerate(ready_nodes):
#             res = node_results[i]
#             results.append(res)
#             output_data_map[node_id] = res["output_data"]
#             execution_order.append(node_id)

#             print(f"[INFO] Node executed: {node_id} -> {res['node']}")

#             for downstream in graph[node_id]:
#                 indegree[downstream] -= 1

#         # Identify new ready nodes (all dependencies satisfied)
#         ready_nodes = [nid for nid, deg in indegree.items() if deg == 0 and nid not in output_data_map]

#     # Cleanup temporary files
#     cleanup_temp_dir()
#     print(f"[INFO] Pipeline execution order: {execution_order}")

#     return {
#         "status": "✅ Pipeline executed successfully",
#         "results": results,
#         "execution_order": execution_order
#     }

async def run_pipeline(pipeline_id: str):
    """
    Executes a saved pipeline with DAG-based parallelism.
    Respects dependencies and runs nodes in the correct order.
    Handles multiple upstream dependencies with merged inputs.
    """
    pipeline = await db.pipelines.find_one({"_id": ObjectId(pipeline_id)})
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")

    # node_id -> node mapping
    nodes = {n: {"node_id": n} for n in pipeline.get("nodes", [])}
    edges = pipeline.get("connections", [])

    # Build dependency graph
    graph = {nid: [] for nid in nodes}       # node -> list of downstream nodes
    indegree = {nid: 0 for nid in nodes}    # node -> number of upstream dependencies
    for edge in edges:
        graph[edge["from"]].append(edge["to"])
        indegree[edge["to"]] += 1

    output_data_map = {}   # node_id -> output data
    execution_order = []
    results = []

    executor = ThreadPoolExecutor(max_workers=4)
    loop = asyncio.get_event_loop()

    # Nodes with no dependencies
    ready_nodes = [nid for nid, deg in indegree.items() if deg == 0]

    print(f"[INFO] Starting pipeline: {pipeline['name']}")
    print(f"[INFO] TEMP_DIR: {TEMP_DIR}")

    while ready_nodes:
        tasks = []

        for node_id in ready_nodes:
            node = nodes[node_id]

            # Fetch script using node_id (node_id = script _id)
            script_doc = await db.scripts.find_one({"_id": ObjectId(node_id)})
            if not script_doc:
                raise HTTPException(status_code=400, detail=f"Missing script for node {node_id}")

            # Collect outputs from direct upstream dependencies
            # prev_outputs = [
            #     output_data_map[src] 
            #     for src, outs in graph.items() 
            #     if node_id in outs and src in output_data_map
            # ]
            prev_outputs = [
                output_data_map[src] for src, outs in graph.items() if node_id in outs and src in output_data_map
            ]


            # Merge all upstream outputs safely
            # merged_input = {}
            # for out in prev_outputs:
            #     if not out:
            #         continue
            #     if isinstance(out, dict):
            #         # If dict has a 'data' list, extend it
            #         if "data" in out and isinstance(out["data"], list):
            #             merged_input.setdefault("data", []).extend(out["data"])
            #         else:
            #             merged_input.update(out)
            #     elif isinstance(out, list):
            #         merged_input.setdefault("data", []).extend(out)
            import copy

            merged_input = {}
            for out in prev_outputs:
                if not out:
                    continue
                if isinstance(out, dict):
                    merged_input.update(copy.deepcopy(out))
                elif isinstance(out, list):
                    merged_input.setdefault("data", []).extend(copy.deepcopy(out))


            # Schedule node execution in thread pool
            tasks.append(loop.run_in_executor(executor, execute_node, script_doc, merged_input))

        # Wait for all ready nodes to complete
        node_results = await asyncio.gather(*tasks)

        # Update results and downstream dependencies
        for i, node_id in enumerate(ready_nodes):
            res = node_results[i]
            results.append(res)
            output_data_map[node_id] = res["output_data"]
            execution_order.append(node_id)

            print(f"[INFO] Node executed: {node_id} -> {res['node']}")

            for downstream in graph[node_id]:
                indegree[downstream] -= 1

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
async def save_pipeline_to_db(name: str, description: str, nodes: list, connections: list):
    pipeline_doc = {
        "name": name,
        "description": description,
        "nodes": nodes,
        "connections": connections,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    result = await db.pipelines.insert_one(pipeline_doc)
    return {"status": "✅ Pipeline saved successfully", "pipeline_id": str(result.inserted_id)}
