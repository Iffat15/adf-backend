import json
import os

data = INPUT_DATA.get("data", []) if isinstance(INPUT_DATA, dict) else INPUT_DATA
print(data)
# For demo, just print
print(f"✅ L1: Loading {len(data)} records")
for d in data:
    print(d)

# Optionally, save to final output file
with open(OUTPUT_PATH, "w") as f:
    json.dump({"data": data}, f, indent=2)

print(f"✅ L1: Data loaded -> {OUTPUT_PATH}")
