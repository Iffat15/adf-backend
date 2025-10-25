import json
import os

data = INPUT_DATA.get("data", []) if isinstance(INPUT_DATA, dict) else INPUT_DATA

# Rename keys to standard format
mapped = []
for d in data:
    mapped.append({
        "id": d.get("order_id"),
        "customer_id": d.get("customer_id"),
        "total_amount": d.get("amount")
    })

with open(OUTPUT_PATH, "w") as f:
    json.dump({"data": mapped}, f, indent=2)

print(f"✅ T2: Mapped orders data -> {OUTPUT_PATH}")
