import json, os

TEMP_DIR = "temp_data"
os.makedirs(TEMP_DIR, exist_ok=True)

def transform_data(input_file):
    with open(input_file, "r") as f:
        data = json.load(f)
    # Example transformation: add 'is_adult' field
    for item in data:
        item["is_adult"] = item["age"] >= 18
    return data

if __name__ == "__main__":
    # Automatically pick the last file in temp_data
    input_file = sorted(os.listdir(TEMP_DIR))[-1]
    input_path = os.path.join(TEMP_DIR, input_file)

    transformed = transform_data(input_path)
    output_file = os.path.join(TEMP_DIR, f"{input_file}")
    with open(output_file, "w") as f:
        json.dump(transformed, f, indent=2)
    print(f"✅ Transformed data saved to {output_file}")
