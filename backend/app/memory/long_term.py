from datetime import datetime, UTC
from backend.app.database.mongodb import database

memory_collection = database["long_term_memory"]

async def save_user_memory(user_id:str, memory:str):
    existing_memory = await memory_collection.find_one({"user_id":user_id,"memory":memory})
    
    if existing_memory:
        return
    memory_doc = {
        "user_id":user_id,
        "memory":memory,
        "timestamp":datetime.now(UTC)
    }
    await memory_collection.insert_one(memory_doc)

async def get_user_memories(user_id:str,limit:int=10):
    convo = (memory_collection.find_one({"user_id":user_id}).sort("timestamp",-1).limit(limit))

    memories = []
    async for memory in convo:
        memories.append(memory["memory"])
    memories.reverse()

    return memories

async def build_long_term_context(user_id:str):
    memories = await get_user_memories(user_id)

    if not memories:
        return ""
    
    context = "User Memory:\n"
    for memory in memories:
        context += f"- {memory}\n"
    return context.strip()