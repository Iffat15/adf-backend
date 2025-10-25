from db.ssms_connectors import get_sqlserver_engine
from sqlalchemy import text
def test_connection():
    try:
        engine = get_sqlserver_engine()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT @@VERSION;"))
            print("✅ Connected to SQL Server. Version:", result.fetchone()[0])
    except Exception as e:
        print("❌ Connection failed:", e)

if __name__ == "__main__":
    test_connection()
