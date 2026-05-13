from fastapi import APIRouter

router = APIRouter(
    prefix = "/chat",
    tags=['Chat']
)

@router.get("/")
async def chat_test():
    return{
        "message":"Chat route working"
    }