import json
import os

# Simulate extraction from a database or file
data = [
    {"customer_id": 1, "name": "Alice", "age": 25},
    {"customer_id": 2, "name": "Bob", "age": None},  # intentionally dirty
    {"customer_id": 3, "name": "Charlie", "age": 30}
]

with open(OUTPUT_PATH, "w") as f:
    json.dump({"data": data}, f, indent=2)

print(f"✅ E1: Extracted customer data -> {OUTPUT_PATH}")
