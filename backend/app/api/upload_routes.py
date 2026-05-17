import os
import uuid
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException

from backend.app.auth.dependencies import get_current_user
from backend.app.services.document_service import process_upload_document
from backend.app.database.mongodb import database
from datetime import datetime, UTC
documents_collection = database["documents"]

router = APIRouter(
    prefix = "/upload",
    tags=['Upload']
)

UPLOAD_DIR =  "backend/app/uploads"
os.makedirs(UPLOAD_DIR,exist_ok=True)


@router.post("/pdf")
async def upload_pdf(file:UploadFile=File(...),
current_user: dict = Depends(get_current_user)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail='Only PDF files allowed'
        )
    user_id = str(current_user["_id"])

    user_folder = os.path.join(UPLOAD_DIR, user_id)
    os.makedirs(user_folder,exist_ok=True)

    unique_filename = f"{uuid.uuid4()}.pdf"

    file_path = os.path.join(user_folder, unique_filename)

    with open(file_path,"wb") as f:
        content = await file.read()
        f.write(content)

    await process_upload_document(
        file_path=file_path,
        user_id=user_id,
        filename=file.filename
    )
   
    await documents_collection.insert_one({

    "user_id": user_id,

    "original_filename":
        file.filename,

    "stored_filename":
        unique_filename,

    "path":
        file_path,

    "uploaded_at":
        datetime.now(UTC)
})
    return{
        "message":"PDF uploaded succssfully."
    }