from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

class Database:
    client: AsyncIOMotorClient = None
    db = None

db = Database()

import certifi

async def connect_to_mongo():
    try:
        # Using certifi's CA bundle with a fallback to allow invalid certificates
        ca = certifi.where()
        db.client = AsyncIOMotorClient(
            MONGO_URI, 
            tlsCAFile=ca, 
            tlsAllowInvalidCertificates=True, 
            serverSelectionTimeoutMS=5000
        )
        db.db = db.client[DB_NAME]
        # Force a connection check
        await db.client.admin.command('ping')
        print("Successfully connected to MongoDB Atlas")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        print("IMPORTANT: Check if your IP address is whitelisted in MongoDB Atlas.")

async def close_mongo_connection():
    if db.client:
        db.client.close()
        print("Closed MongoDB connection")

def get_database():
    return db.db
