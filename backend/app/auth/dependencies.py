from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError

from backend.app.config.settings import settings
from backend.app.database.mongodb import get_database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str=Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        email = payload.get("email")

        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid Token"
            )
        db = get_database()
        user = await db.users.find_one(
            {"email": email}
        )

        if user is None:

            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return user

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Token verification failed"
        )