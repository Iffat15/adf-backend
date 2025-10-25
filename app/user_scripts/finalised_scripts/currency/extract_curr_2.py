import json
import os

# Simulated extract source — replace with actual source logic (e.g., file, API, DB)
extracted_data = [
    {"order_id": 101, "user_id": 1, "price": 250},
    {"order_id": 102, "user_id": 2, "price": 450},
    {"order_id": 103, "user_id": 1, "price": 125}
]

# Wrap in expected pipeline format
extract_output = {
    "data": extracted_data
}

# Save to output file
with open(OUTPUT_PATH, "w") as f:
    json.dump(extract_output, f, indent=2)

print(f"✅ Extract Node executed -> {OUTPUT_PATH}")
print(f"Rows extracted: {len(extracted_data)}")
print("Ready for currency transformation in next node.")
