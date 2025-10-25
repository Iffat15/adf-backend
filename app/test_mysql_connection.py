
import urllib
from sqlalchemy import create_engine

def get_engine(database_name="EXAM"):
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


from sqlalchemy import text

def test_sql_server_connection():
    engine = get_engine("EXAM")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT @@VERSION"))
            print("✅ Connected to SQL Server. Version:", result.fetchone()[0])
    except Exception as e:
        print("❌ Connection failed:", e)

if __name__ == "__main__":
    test_sql_server_connection()

