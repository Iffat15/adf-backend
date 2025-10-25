# import os
# import json
# from dotenv import load_dotenv

# load_dotenv()

# def load_db_config():
#     with open("config/db_connections.json") as f:
#         return json.load(f)

# def get_connection_string(db_type):
#     config = load_db_config()[db_type]

#     if db_type == "postgresql":
#         return f"postgresql://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}@{config['host']}:{config['port']}/{config['database']}"
#     elif db_type == "sql_server":
#         return f"mssql+pyodbc://{os.getenv('MSSQL_USER')}:{os.getenv('MSSQL_PASSWORD')}@{config['host']}:{config['port']}/{config['database']}?driver=ODBC+Driver+17+for+SQL+Server"
#     elif db_type == "mysql":
#         return f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{config['host']}:{config['port']}/{config['database']}"
#     else:
#         raise ValueError(f"Unsupported DB type: {db_type}")
import pymysql
import os
import json
from dotenv import load_dotenv

load_dotenv()

def load_db_config():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # goes up from db/ to app/
    config_path = os.path.join(base_dir, "config", "db_connections.json")
    with open(config_path) as f:
        return json.load(f)


def connect_mysql(database_name):
    config = load_db_config()["mysql"]
    connection = pymysql.connect(
        host=config["host"],
        port=config["port"],
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=database_name
    )
    return connection

def get_engine(database_name):
    """
    Returns a SQLAlchemy engine for the specified SQL Server database.
    Default is 'EXAM'. You can pass 'TESTDB' or any other name as needed.
    """
    params = urllib.parse.quote_plus(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER=localhost\\SQLEXPRESS;"
        f"DATABASE={database_name};"
        f"Trusted_Connection=yes;"
    )
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
    # if engine:
    #     print("conn made successfully")
    return engine