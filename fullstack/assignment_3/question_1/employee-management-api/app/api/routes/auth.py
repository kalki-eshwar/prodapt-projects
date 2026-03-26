from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.controllers.auth_controller import (
    login_controller,
    register_admin_controller,
    register_controller,
)
from app.core.dependencies import get_db
from app.schemas.auth_schema import AuthResponse, LoginRequest, RegisterAdminRequest, RegisterRequest


router = APIRouter()


@router.post(
    "/register",
    response_model=AuthResponse,
    responses={
        400: {
            "description": "Invalid JSON body",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid JSON body. Use double quotes for keys/values and no trailing commas.",
                        "example": {
                            "email": "admin@example.com",
                            "password": "admin123",
                            "role": "admin",
                        },
                    }
                }
            },
        }
    },
)
async def register(payload: RegisterRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    return await register_controller(payload, db)


@router.post(
    "/register-admin",
    response_model=AuthResponse,
    responses={
        400: {
            "description": "Invalid JSON body",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid JSON body. Use double quotes for keys/values and no trailing commas.",
                        "example": {
                            "email": "admin@example.com",
                            "password": "admin123",
                        },
                    }
                }
            },
        }
    },
)
async def register_admin(payload: RegisterAdminRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    return await register_admin_controller(payload, db)


@router.post(
    "/login",
    response_model=AuthResponse,
    responses={
        400: {
            "description": "Invalid JSON body",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid JSON body. Use double quotes for keys/values and no trailing commas.",
                        "example": {
                            "email": "admin@example.com",
                            "password": "admin123",
                        },
                    }
                }
            },
        }
    },
)
async def login(payload: LoginRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    return await login_controller(payload, db)
