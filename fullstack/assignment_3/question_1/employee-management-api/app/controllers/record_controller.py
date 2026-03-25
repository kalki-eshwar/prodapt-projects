from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repositories.employee_repository import EmployeeRepository
from app.repositories.record_repository import RecordRepository
from app.services.record_service import RecordService


def _service(db: AsyncIOMotorDatabase) -> RecordService:
    return RecordService(RecordRepository(db), EmployeeRepository(db))


async def create_record_controller(user_id: str, payload: dict, db: AsyncIOMotorDatabase) -> dict:
    return await _service(db).create_record(user_id, payload)


async def my_records_controller(user_id: str, db: AsyncIOMotorDatabase) -> list[dict]:
    return await _service(db).get_my_records(user_id)


async def all_records_controller(filters: dict, db: AsyncIOMotorDatabase) -> list[dict]:
    return await _service(db).list_records(filters)


async def approve_record_controller(record_id: str, db: AsyncIOMotorDatabase) -> dict:
    return await _service(db).approve_leave(record_id)


async def reject_record_controller(record_id: str, db: AsyncIOMotorDatabase) -> dict:
    return await _service(db).reject_leave(record_id)
