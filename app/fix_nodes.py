import asyncio
from db_config import db

async def fix_nodes():
    result = await db["scripts"].update_many(
        {"type": {"$exists": False}},
        {"$set": {"type": "extract"}}  # or any default you want
    )
    print(f"Modified {result.modified_count} nodes")

if __name__ == "__main__":
    asyncio.run(fix_nodes())
