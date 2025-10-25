
import json
import os
import pandas as pd

# Extract input data safely
input_data_list = INPUT_DATA.get("data", []) if isinstance(INPUT_DATA, dict) else INPUT_DATA

# Extract node parameters
params = NODE_PARAMS or {}  # <-- use NODE_PARAMS passed from backend
col1 = params.get("col1")
col2 = params.get("col2")
join_type = params.get("join_type", "inner")  # default to inner join

if not col1 or not col2:
    raise Exception("❌ Missing 'col1' or 'col2' in node params for merge.")

# Expecting input_data_list to be a list of two datasets: [input1, input2]
if len(input_data_list) < 2:
    raise Exception("❌ Merge node expects 2 inputs (input1 and input2).")

df1 = pd.DataFrame(input_data_list[0].get("data", []))
df2 = pd.DataFrame(input_data_list[1].get("data", []))

# Merge based on user-specified columns and join type
merged_df = pd.merge(df1, df2, left_on=col1, right_on=col2, how=join_type)

# Convert merged dataframe back to list of dicts
merged_output = {"data": merged_df.to_dict(orient="records")}

# Save to output file
with open(OUTPUT_PATH, "w") as f:
    json.dump(merged_output, f, indent=2)

print(f"✅ Transform Merge executed -> {OUTPUT_PATH}")
print(f"Columns merged: input1.{col1} <-> input2.{col2}, join type: {join_type}")
print(f"Rows after merge: {len(merged_output['data'])}")
