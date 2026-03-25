from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserModel(BaseModel):
    id: str | None = None
    email: EmailStr
    password: str
    role: str
    created_at: datetime | None = None
