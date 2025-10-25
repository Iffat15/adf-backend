
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os, json
from sqlalchemy import create_engine

def load_db_config():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "db_connections.json")
    with open(config_path) as f:
        return json.load(f)

def connect_postgresql():
    load_dotenv()
    config = load_db_config()["postgresql"]

    user = os.getenv("PG_USER")
    raw_password = os.getenv("PG_PASSWORD")
    password = quote_plus(raw_password)  # Encode special characters

    host = config["host"]
    port = config["port"]
    database = config["database"]

    conn_str = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(conn_str)

    return engine
