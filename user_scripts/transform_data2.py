# import json
# import os

# data = INPUT_DATA  # backend injects this variable

# for d in data:
#     d["is_adult"] = d["age"] >= 18

# with open(OUTPUT_PATH, "w") as f:
#     json.dump(data, f)
# print("✅ Transformed data and saved to", OUTPUT_PATH)
import json
import os

# Safely get input data
data = INPUT_DATA.get("data") if isinstance(INPUT_DATA, dict) else INPUT_DATA

if not isinstance(data, list):
    data = []

# Transformation
for d in data:
    d["is_adult"] = d.get("age", 0) >= 18

# Wrap output in dict so downstream nodes can merge safely
output_data = {"data": data}

# Save to OUTPUT_PATH
with open(OUTPUT_PATH, "w") as f:
    json.dump(output_data, f, indent=2)

print(f"✅ Transformed {len(data)} records and saved to {OUTPUT_PATH}")
