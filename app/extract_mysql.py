# import sys
# import json
# from sqlalchemy import text
# from test_mysql_connection import get_engine  # Adjust if needed
# import os
# import datetime

# def default_serializer(obj):
#     if isinstance(obj, (datetime.date, datetime.datetime)):
#         return obj.isoformat()
#     raise TypeError(f"Type {type(obj)} not serializable")

# def extract_table_to_json(database_name, table_name):
#     try:
#         engine = get_engine(database_name)
#         with engine.connect() as conn:
#             result = conn.execute(text(f"SELECT * FROM {table_name}"))
#             # rows = [dict(row) for row in result]
#             rows = [dict(row._mapping) for row in result]


#         extract_output = {"data": rows}
#         print(extract_output)
#         # with open(OUTPUT_PATH, "w") as f:
#         #     # json.dump(extract_output, f, indent=2)
#         #     json.dump(extract_output, f, indent=2, default=default_serializer)


#         # print(f"✅ Extract Node executed -> {OUTPUT_PATH}")
#         print(f"Rows extracted: {len(rows)}")
#         print("Ready for transformation in next node.")
#     except Exception as e:
#         print(f"❌ Extraction failed: {e}")

# if __name__ == "__main__":
#     # These variables are expected to be passed in by the pipeline
#     # params = NODE_PARAMS or {}  # <-- use NODE_PARAMS passed from backend
#     database_name = "sales_Ind"
#     table_name = "SalesDataIndia"
#     # output_path = os.getenv("OUTPUT_PATH")

#     if not all([database_name, table_name]):
#         print("❌ Missing required parameters: database_name, table_name, OUTPUT_PATH")
#     else:
#         extract_table_to_json(database_name, table_name)
import sys
import json
import os
import datetime, decimal
from sqlalchemy import text
from db.connectors import connect_mysql  # Make sure path is correct

def default_serializer(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    if isinstance(obj, decimal.Decimal):
        return float(obj)  # or str(obj) if you prefer
    raise TypeError(f"Type {type(obj)} not serializable")

def extract_table_to_json(database_name, table_name):
    try:
        conn = connect_mysql(database_name)
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name}")
            columns = [desc[0] for desc in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        extract_output = {"data": rows}
        print(json.dumps(extract_output, indent=2, default=default_serializer))

        print(f"✅ Extract Node executed successfully")
        print(f"Rows extracted: {len(rows)}")
        print("Ready for transformation in next node.")
    except Exception as e:
        print(f"❌ Extraction failed: {type(e).__name__} - {e}")

if __name__ == "__main__":
    database_name = "exam"
    table_name = "coffeesales"

    extract_table_to_json(database_name, table_name)
