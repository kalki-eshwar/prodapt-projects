from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repositories.employee_repository import EmployeeRepository
from app.repositories.record_repository import RecordRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.employee_service import EmployeeService
from app.services.record_service import RecordService


async def create_employee_admin_controller(payload: dict, db: AsyncIOMotorDatabase) -> dict:
    auth_service = AuthService(UserRepository(db))
    employee_service = EmployeeService(EmployeeRepository(db), UserRepository(db))

    auth_result = await auth_service.register(payload["email"], payload["password"], payload["role"])
    created_user = await UserRepository(db).get_by_email(payload["email"])
    employee = await employee_service.create_employee(
        user_id=created_user["id"],
        name=payload["name"],
        department=payload["department"],
        manager_id=payload.get("manager_id"),
    )
    return {"employee": employee, "user_role": auth_result["role"]}


async def update_employee_admin_controller(employee_id: str, payload: dict, db: AsyncIOMotorDatabase) -> dict:
    employee_service = EmployeeService(EmployeeRepository(db), UserRepository(db))
    return await employee_service.update_employee(employee_id, payload)


async def delete_employee_admin_controller(employee_id: str, db: AsyncIOMotorDatabase) -> dict:
    employee_service = EmployeeService(EmployeeRepository(db), UserRepository(db))
    deleted = await employee_service.delete_employee(employee_id)
    return {"deleted": deleted}


async def report_admin_controller(db: AsyncIOMotorDatabase) -> dict:
    record_service = RecordService(RecordRepository(db), EmployeeRepository(db))
    employees = await EmployeeRepository(db).list_all()
    record_summary = await record_service.report_summary()
    return {
        "total_employees": len(employees),
        **record_summary,
    }
