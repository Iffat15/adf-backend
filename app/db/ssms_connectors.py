import os
import json
import urllib
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

def load_db_config():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "db_connections.json")
    with open(config_path) as f:
        return json.load(f)

def get_engine(database_name):
    config = load_db_config()["sql_server"]
    instance = config.get("instance", os.getenv("SQLSERVER_INSTANCE", "SQLEXPRESS"))
    conn_str = urllib.parse.quote_plus(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={config['host']}\\{instance};"
        f"DATABASE={database_name};"
        f"Trusted_Connection=yes;"
    )
    return create_engine(f"mssql+pyodbc:///?odbc_connect={conn_str}")
