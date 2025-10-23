import json
import os

# INPUT_DATA is either:
# 1) A list of upstream outputs (dicts) or
# 2) A merged dict with "data" key (depending on T3)
# We'll handle both

customers = []
orders = []

# Ensure INPUT_DATA is always a list of dicts
upstreams = INPUT_DATA if isinstance(INPUT_DATA, list) else [INPUT_DATA]

for upstream in upstreams:
    if isinstance(upstream, dict) and "data" in upstream:
        # check keys in first row safely
        first_row = upstream["data"][0] if upstream["data"] else {}
        if "email" in first_row:
            customers = upstream["data"]
        else:
            orders = upstream["data"]

# Join on customer_id
joined = []
for c in customers:
    for o in orders:
        if c.get("customer_id") == o.get("customer_id"):
            joined.append({**c, **o})  # fixed syntax

# Write output
with open(OUTPUT_PATH, "w") as f:
    json.dump({"data": joined}
    )