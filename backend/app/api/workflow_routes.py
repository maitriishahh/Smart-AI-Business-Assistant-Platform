from fastapi import APIRouter

router = APIRouter(
    prefix="/workflow",
    tags=['Workflow']
)

@router.get("/")
async def workflow_test():
    return{
        "mesaage": "Workflow route working"
    }