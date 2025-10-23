import json
import os

data = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30},
    {"name": "Charlie", "age": 22},
]

output = {"data": data}

with open(OUTPUT_PATH, "w") as f:
    json.dump(output, f, indent=2)

print(f"✅ Extracted data and saved to {OUTPUT_PATH}")
