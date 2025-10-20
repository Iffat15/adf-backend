import json
import os

data = INPUT_DATA  # backend injects this variable

for d in data:
    d["is_adult"] = d["age"] >= 18

with open(OUTPUT_PATH, "w") as f:
    json.dump(data, f)
print("✅ Transformed data and saved to", OUTPUT_PATH)
