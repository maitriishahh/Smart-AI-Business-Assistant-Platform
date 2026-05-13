from fastapi import APIRouter

router = APIRouter(
    prefix = "/upload",
    tags=['Upload']
)

@router.get("/")
async def upload_test():
    return{
        "message":"Upload route working"
    }