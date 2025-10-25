import json
import os

# Example orders data from Source 2
data = [
    {"order_id": 101, "user_id": 1, "amount": 250},
    {"order_id": 102, "user_id": 2, "amount": 450},
    {"order_id": 103, "user_id": 1, "amount": 125}
]

# Save to output file specified by backend
with open(OUTPUT_PATH, "w") as f:
    json.dump({"data": data}, f, indent=2)

print(f"✅ E2: Extracted orders data -> {OUTPUT_PATH}")
