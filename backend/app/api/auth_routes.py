from fastapi import APIRouter, HTTPException
from backend.app.database.mongodb import get_database

from backend.app.models.user_model import (UserSignup,UserLogin)

from backend.app.auth.hashing import (hash_pwd,verify_pwd)

from backend.app.auth.jwt_handler import (create_access_token)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/signup")
async def signup(user: UserSignup):

    try:

        db = get_database()

        # CHECK EXISTING USER
        existing_user = await db.users.find_one(
            {"email": user.email}
        )

        if existing_user:

            raise HTTPException(
                status_code=400,
                detail="User already exists"
            )

        # HASH PASSWORD
        hashed_password = hash_pwd(user.password)

        # USER DATA
        user_data = {
            "name": user.name,
            "email": user.email,
            "password": hashed_password
        }

        # INSERT USER
        await db.users.insert_one(user_data)

        return {
            "success": True,
            "message": "User registered successfully"
        }

    except HTTPException as http_error:

        raise http_error

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Signup failed: {str(e)}"
        )
    
@router.post("/login")
async def login(user: UserLogin):

    try:

        db = get_database()

        # FIND USER
        existing_user = await db.users.find_one(
            {"email": user.email}
        )

        if not existing_user:

            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        # VERIFY PASSWORD
        password_valid = verify_pwd(
            user.password,
            existing_user["password"]
        )

        if not password_valid:

            raise HTTPException(
                status_code=401,
                detail="Invalid password"
            )

        # GENERATE JWT TOKEN
        access_token = create_access_token(
            data={
                "email": existing_user["email"]
            }
        )

        return {
            "success": True,
            "access_token": access_token,
            "token_type": "bearer"
        }

    except HTTPException as http_error:

        raise http_error

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Login failed: {str(e)}"
        )