from fastapi import (
    APIRouter,
    Depends
)

from pydantic import BaseModel

from backend.app.auth.dependencies import (
    get_current_user
)

from backend.app.models.chat_model import (ChatRequest)

from backend.app.services.chat_service import (
    ask_question
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post("/query")
async def chat_query(
    payload: ChatRequest,
    current_user: dict = Depends(get_current_user)
):

    answer = await ask_question(
        message=payload.message,
        session_id=payload.session_id,
        user_id=str(current_user["_id"])
    )

    return answer