import json, os

TEMP_DIR = "temp_data"
os.makedirs(TEMP_DIR, exist_ok=True)

def load_data(input_file):
    with open(input_file, "r") as f:
        data = json.load(f)
    # For simplicity, just print each record
    print("Final data to load:")
    for record in data:
        print(record)

if __name__ == "__main__":
    input_file = sorted(os.listdir(TEMP_DIR))[-1]
    input_path = os.path.join(TEMP_DIR, input_file)
    load_data(input_path)
    print(f"✅ Data loaded successfully from {input_path}")
