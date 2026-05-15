from datetime import datetime, UTC
from backend.app.database.mongodb import database

conversation_collection = database["conversations"]

async def save_convo(user_id: str, session_id: str, user_msg:str, assistant_response: str):

    conversation = {
        "user_id": user_id,
        "session_id": session_id,
        "user_msg": user_msg,
        "assistant_response": assistant_response,
        "timestamp": datetime.now(UTC)
    }

    await conversation_collection.insert_one(conversation)

async def get_recent_conversations(user_id: str, limit: int=5):
    convo = (conversation_collection.find({"user_id":user_id}).sort("timetamp",-1).limit(limit))

    conversations = []

    async for conversation in convo:
        conversations.append({
            "user_msg":conversation['user_msg'],
            "assistant_response":conversation['assistant_response']
        })
    conversations.reverse()
    return conversations