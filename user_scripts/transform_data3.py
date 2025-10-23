import json
import os

# Get injected data safely
if isinstance(INPUT_DATA, dict):
    data = INPUT_DATA.get("data", [])
else:
    data = INPUT_DATA

# Ensure data is a list
if not isinstance(data, list):
    data = []

# Transform each record
for d in data:
    if isinstance(d, dict):
        d["is_adult"] = d.get("age", 0) >= 18

# Prepare consistent output
output = {"data": data}

# Write output JSON
with open(OUTPUT_PATH, "w") as f:
    json.dump(output, f, indent=2)

print(f"✅ Transformed {len(data)} records and saved to {OUTPUT_PATH}")
