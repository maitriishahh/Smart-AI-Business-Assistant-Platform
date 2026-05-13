from motor.motor_asyncio import AsyncIOMotorClient
from backend.app.config.settings import Settings

client = AsyncIOMotorClient(Settings.MONGODB_URL)
database = client[Settings.DATABASE_NAME]

def get_database():
    return database