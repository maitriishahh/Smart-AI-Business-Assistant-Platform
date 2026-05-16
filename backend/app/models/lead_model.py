from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, UTC

class Lead(BaseModel):
    name: Optional[str] = None
    company: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    requirements: Optional[str] = None
    budget: Optional[str] = None
    classification: Optional[str] = "cold"
    created_at: datetime = datetime.now(UTC)