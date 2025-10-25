import os
import sys
import json
from sqlalchemy import text
from app.db.connectors import get_engine  # adjust path if needed

def load_json_to_table(database_name, table_name):
    try:
        # Read data from JSON file
        with open(INPUT_PATH, "r") as f:
            payload = json.load(f)

        rows = payload.get("data", [])
        if not rows:
            print(f"⚠️ No data found in {INPUT_PATH}")
            return

        engine = get_engine(database_name)
        with engine.connect() as conn:
            for row in rows:
                columns = ", ".join(row.keys())
                placeholders = ", ".join([f":{key}" for key in row.keys()])
                insert_stmt = text(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})")
                conn.execute(insert_stmt, row)

        print(f"✅ Load Node executed -> {table_name} in {database_name}")
        print(f"Rows loaded: {len(rows)}")
        print("Ready for next pipeline step.")
    except Exception as e:
        print(f"❌ Load failed: {e}")

if __name__ == "__main__":
    database_name = os.getenv("database_name")
    table_name = os.getenv("table_name")
    input_path = os.getenv("INPUT_PATH")

    if not all([database_name, table_name]):
        print("❌ Missing required parameters: database_name, table_name, INPUT_PATH")
    else:
        load_json_to_table(database_name, table_name)
