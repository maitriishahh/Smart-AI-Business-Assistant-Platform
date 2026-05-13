from fastapi import APIRouter

router = APIRouter(
    prefix = "/lead",
    tags=['Lead']
)

@router.get("/")
async def lead_test():
    return{
        "message":"Lead route working"
    }