from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm
from backend.app.database.mongodb import get_database

from backend.app.models.user_model import (UserSignup,UserLogin)

from backend.app.auth.hashing import (hash_pwd,verify_pwd)

from backend.app.auth.jwt_handler import (create_access_token)

from backend.app.auth.dependencies import (
    get_current_user
)

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
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    try:

        db = get_database()

        existing_user = await db.users.find_one(
            {"email": form_data.username}
        )

        if not existing_user:

            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        password_valid = verify_pwd(
            form_data.password,
            existing_user["password"]
        )

        if not password_valid:

            raise HTTPException(
                status_code=401,
                detail="Invalid password"
            )

        access_token = create_access_token(
            data={
                "email": existing_user["email"]
            }
        )

        return {
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

@router.get("/profile")
async def get_profile(
    current_user=Depends(get_current_user)
):

    return {
        "name": current_user["name"],
        "email": current_user["email"]
    }
