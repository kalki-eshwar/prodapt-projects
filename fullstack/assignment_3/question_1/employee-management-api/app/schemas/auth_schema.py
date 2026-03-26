from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    role: Literal["employee", "manager", "admin"] = "employee"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "admin@example.com",
                "password": "admin123",
                "role": "admin",
            }
        }
    )


class RegisterAdminRequest(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "admin@example.com",
                "password": "admin123",
            }
        }
    )


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "admin@example.com",
                "password": "admin123",
            }
        }
    )


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
