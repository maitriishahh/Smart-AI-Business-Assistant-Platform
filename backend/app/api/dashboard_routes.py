from fastapi import APIRouter
from backend.app.database.mongodb import get_database

router = APIRouter(
    prefix = "/dashboard",
    tags=['Dashboard']
)

@router.get("/")
async def dashboard_test():

    db=get_database()
    collections = await db.list_collection_names()
    
    return{
        "message":"MongoDB connected successfully",
        "collections":collections
    }