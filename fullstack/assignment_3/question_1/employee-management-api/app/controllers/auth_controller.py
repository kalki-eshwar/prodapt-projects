from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repositories.employee_repository import EmployeeRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import LoginRequest, RegisterAdminRequest, RegisterRequest
from app.services.auth_service import AuthService


async def register_controller(payload: RegisterRequest, db: AsyncIOMotorDatabase) -> dict:
    service = AuthService(UserRepository(db), EmployeeRepository(db))
    return await service.register(payload.email, payload.password, payload.role)


async def register_admin_controller(payload: RegisterAdminRequest, db: AsyncIOMotorDatabase) -> dict:
    service = AuthService(UserRepository(db), EmployeeRepository(db))
    return await service.register(payload.email, payload.password, "admin")


async def login_controller(payload: LoginRequest, db: AsyncIOMotorDatabase) -> dict:
    service = AuthService(UserRepository(db), EmployeeRepository(db))
    return await service.login(payload.email, payload.password)
