# from motor.motor_asyncio import AsyncIOMotorClient
# import asyncio

# MONGODB_URL = "mongodb+srv://maitri:maitri14@cluster0.cl6lgpt.mongodb.net/?appName=Cluster0"

# async def test():
#     client = AsyncIOMotorClient(MONGODB_URL)
    
#     dbs = await client.list_database_names()
    
#     print("Connected successfully!")
#     print(dbs)

# asyncio.run(test())

# from backend.app.config.settings import Settings

# print("Mongo URL:", Settings.MONGODB_URL)
# print("Database:", Settings.DATABASE_NAME)
# print("Gemini Key:", Settings.GEMINI_API_KEY)

from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

hashed = pwd_context.hash("maitri123")

print(hashed)