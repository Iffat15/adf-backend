import json, os
from bson import ObjectId

TEMP_DIR = "temp_data"
os.makedirs(TEMP_DIR, exist_ok=True)

def extract_data():
    data = [
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 30},
        {"name": "Charlie", "age": 22}
    ]
    return data

if __name__ == "__main__":
    extracted = extract_data()
    output_file = os.path.join(TEMP_DIR, f"{ObjectId()}.json")
    with open(output_file, "w") as f:
        json.dump(extracted, f, indent=2)
    print(f"✅ Extracted data saved to {output_file}")
