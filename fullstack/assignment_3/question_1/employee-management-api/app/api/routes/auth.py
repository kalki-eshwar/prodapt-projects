from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.controllers.auth_controller import login_controller, register_controller
from app.core.dependencies import get_db
from app.schemas.auth_schema import AuthResponse, LoginRequest, RegisterRequest


router = APIRouter()


@router.post("/register", response_model=AuthResponse)
async def register(payload: RegisterRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    return await register_controller(payload, db)


@router.post("/login", response_model=AuthResponse)
async def login(payload: LoginRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    return await login_controller(payload, db)
