from datetime import datetime, UTC
from backend.app.database.mongodb import database


conversation_collection = database["conversations"]


async def get_convo_context(
    user_id: str,
    limit: int = 5
):

    cursor = (
        conversation_collection
        .find({"user_id": user_id})
        .sort("timestamp", -1)
        .limit(limit)
    )

    conversations = []

    async for convo in cursor:

        conversations.append({

    "user":

        convo.get(
            "user_message",

            convo.get(
                "user_msg",
                ""
            )
        ),

    "assistant":

        convo.get(
            "assistant_response",
            ""
        )
})

    conversations.reverse()

    return conversations


async def update_convo_context(
    user_id: str,
    session_id: str,
    user_msg: str,
    assistant_response: str
):

    conversation = {
        "user_id": user_id,
        "session_id": session_id,
        "user_message": user_msg,
        "assistant_response": assistant_response,
        "timestamp": datetime.now(UTC)
    }

    await conversation_collection.insert_one(conversation)