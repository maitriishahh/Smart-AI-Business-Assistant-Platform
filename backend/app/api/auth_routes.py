from fastapi import APIRouter

router = APIRouter(
    prefix = "/auth",
    tags=['Authentication']
)

@router.get("/")
async def auth_test():
    return{
        "message":"Auth route working"
    }