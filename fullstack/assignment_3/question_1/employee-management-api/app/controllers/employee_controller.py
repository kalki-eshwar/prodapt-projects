from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repositories.employee_repository import EmployeeRepository
from app.repositories.user_repository import UserRepository
from app.services.employee_service import EmployeeService


def _service(db: AsyncIOMotorDatabase) -> EmployeeService:
    return EmployeeService(EmployeeRepository(db), UserRepository(db))


async def get_me_controller(user_id: str, db: AsyncIOMotorDatabase) -> dict:
    return await _service(db).get_my_profile(user_id)


async def update_me_controller(user_id: str, payload: dict, db: AsyncIOMotorDatabase) -> dict:
    return await _service(db).update_my_profile(user_id, payload)


async def list_employees_controller(db: AsyncIOMotorDatabase) -> list[dict]:
    return await _service(db).list_employees()
