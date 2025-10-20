# # from motor.motor_asyncio import AsyncIOMotorClient
# # import os
# # from dotenv import load_dotenv

# # load_dotenv()

# # MONGO_URI = os.getenv("MONGO_URI")
# # DB_NAME = os.getenv("DB_NAME")

# # client = AsyncIOMotorClient(MONGO_URI)
# # db = client[DB_NAME]  # orchpulse_db
# from motor.motor_asyncio import AsyncIOMotorClient
# import os
# from dotenv import load_dotenv
# import asyncio

# load_dotenv()

# MONGO_URI = os.getenv("MONGO_URI")
# DB_NAME = os.getenv("DB_NAME")

# try:
#     client = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=5000)  # 5 sec timeout
#     db = client[DB_NAME]  # orchpulse_db

#     # Async test to check connection
#     async def test_connection():
#         try:
#             # Ping the server
#             await client.admin.command("ping")
#             print("✅ MongoDB connection successful")
#         except Exception as e:
#             print("❌ MongoDB connection failed:", e)

#     asyncio.run(test_connection())

# except Exception as e:
#     print("❌ Could not initialize MongoDB client:", e)
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "orchpulse_db")

# Initialize client and db
client = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client[DB_NAME]

# Async test connection (can be called from FastAPI startup event)
async def test_connection():
    try:
        await client.admin.command("ping")
        print("✅ MongoDB connection successful")
    except Exception as e:
        print("❌ MongoDB connection failed:", e)
