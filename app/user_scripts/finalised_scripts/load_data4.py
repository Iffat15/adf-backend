# import json
# import os

# file = r"adf-backend\app\temp_data\68fc3d5340a4e31e6bcf2731.json"
# file2 = "adf-backend\app\temp_data\dump.json"
# # Load input data
# with open(file, "r") as f:
#     input_data = json.load(f)

# # Access and print the "data" section
# output = json.dumps(input_data["data"], indent=2)
# with open(file2, "w") as f:
#     json.dump({"data": output}, f, indent=2)

# print(output)
import json
import os

# file = r"adf-backend\app\temp_data\68fc3d5340a4e31e6bcf2731.json"
# file2 = r"adf-backend\app\temp_data\dump.json"
INPUT_DATA = INPUT_DATA if 'INPUT_DATA' in globals() else {}
print(INPUT_DATA)
# Load input data
with open(INPUT_DATA, "r") as f:
    input_data = json.load(f)

# Extract the data list
data = input_data.get("data", [])

# Save to new file
with open(OUTPUT_PATH, "w") as f:
    json.dump({"data": data}, f, indent=2)

# Print to console
print(json.dumps(data, indent=2))
