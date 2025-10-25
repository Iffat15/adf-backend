from db.pg_connectors import connect_postgresql
from sqlalchemy import text

def test_connection():
    try:
        engine = connect_postgresql()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            print("✅ Connected to PostgreSQL. Version:", result.fetchone()[0])
    except Exception as e:
        print("❌ Connection failed:", e)

if __name__ == "__main__":
    test_connection()
