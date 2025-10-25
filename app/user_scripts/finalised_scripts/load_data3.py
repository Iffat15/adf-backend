import json
import os

if isinstance(INPUT_DATA, dict):
    data = INPUT_DATA.get("data", [])
else:
    data = INPUT_DATA

print(f"✅ Loaded {len(data)} records")
print(json.dumps(data, indent=2))

# Prepare consistent output
output = {"data": data}

# Write output JSON
with open(OUTPUT_PATH, "w") as f:
    json.dump(output, f, indent=2)

print(f"✅ {len(data)} records and saved to {OUTPUT_PATH}")