import json
import os

data = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30},
    {"name": "Charlie", "age": 22}
]

with open(OUTPUT_PATH, "w") as f:
    json.dump(data, f)
print("✅ Extracted data and saved to", OUTPUT_PATH)
