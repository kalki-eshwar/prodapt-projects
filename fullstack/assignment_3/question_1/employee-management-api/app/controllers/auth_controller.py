from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import LoginRequest, RegisterRequest
from app.services.auth_service import AuthService


async def register_controller(payload: RegisterRequest, db: AsyncIOMotorDatabase) -> dict:
    service = AuthService(UserRepository(db))
    return await service.register(payload.email, payload.password, payload.role)


async def login_controller(payload: LoginRequest, db: AsyncIOMotorDatabase) -> dict:
    service = AuthService(UserRepository(db))
    return await service.login(payload.email, payload.password)
