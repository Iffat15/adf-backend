import json
import os

# INPUT_DATA is a list of upstream outputs, e.g. [T1_output, E2_output]
merged = []

for upstream in INPUT_DATA:
    if isinstance(upstream, dict) and "data" in upstream:
        merged.extend(upstream["data"])
    elif isinstance(upstream, list):  # edge case: list of rows
        merged.extend(upstream)

# Optional: you can also apply column mapping or filtering here
# e.g. renaming keys, aligning columns before join

with open(OUTPUT_PATH, "w") as f:
    json.dump({"data": merged}, f, indent=2)

print(f"✅ T3: Merged T1 + E2 -> {OUTPUT_PATH}")
