
import pandas as pd
from currency_converter import CurrencyConverter
# Safely extract input
INPUT_DATA = INPUT_DATA if 'INPUT_DATA' in globals() else {}
print(INPUT_DATA)
# Handle list of dicts with 'data' key
if isinstance(INPUT_DATA, list) and len(INPUT_DATA) > 0:
    first_item = INPUT_DATA[0]
    print("first item inside input_data is:",first_item)
    if isinstance(first_item, dict) and "data" in first_item:
        rows = first_item["data"]
    else:
        raise Exception("❌ First item in list is not a dict with 'data' key.")
else:
    raise Exception("❌ INPUT_DATA is not a list or is empty.")

# Load into DataFrame
df = pd.DataFrame(rows)
print("dataframe is:",df)
print("📊 Columns in input data:", df.columns.tolist())
cols = df.columns.tolist()

# Extract node parameters
params = NODE_PARAMS or {}  # <-- use NODE_PARAMS passed from backend
column = params.get("column")
from_curr =  params.get("from")
to_curr = params.get("to")
# col2 = params.get("col2")
# join_type = params.get("join_type", "inner")  # default to inner join

for col in cols:
    if col == column:
        print("currency col exists")



c = CurrencyConverter()
df[column] = df[column].apply(lambda x: round(c.convert(x, from_curr, to_curr), 2))

# # Save to output file
# with open(OUTPUT_PATH, "w") as f:
#     json.dump(df, f, indent=2)
import json

# Save to output file
with open(OUTPUT_PATH, "w") as f:
    json.dump(df.to_dict(orient="records"), f, indent=2)

print(f"✅ Converted '{column}' from {from_curr} to {to_curr} and saved to output file.")

print(f"✅ Converted '{column}' from {from_curr} to {to_curr}")
print(df.head())