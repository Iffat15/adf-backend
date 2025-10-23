import json
import os

# Extract input data safely
data = INPUT_DATA.get("data", []) if isinstance(INPUT_DATA, dict) else INPUT_DATA

# Clean null or None values
cleaned = []
for record in data:
    if all(v is not None for v in record.values()):
        cleaned.append(record)

# Save cleaned output
with open(OUTPUT_PATH, "w") as f:
    json.dump({"data": cleaned}, f, indent=2)

print(f"✅ T1: Cleaned null values -> {OUTPUT_PATH}")

