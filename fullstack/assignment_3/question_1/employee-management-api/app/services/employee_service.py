from app.exceptions.custom_exceptions import NotFoundException, ValidationException
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.user_repository import UserRepository


class EmployeeService:
    def __init__(self, employee_repository: EmployeeRepository, user_repository: UserRepository):
        self.employee_repository = employee_repository
        self.user_repository = user_repository

    async def get_my_profile(self, user_id: str) -> dict:
        profile = await self.employee_repository.get_by_user_id(user_id)
        if not profile:
            raise NotFoundException("Employee profile not found")
        return profile

    async def update_my_profile(self, user_id: str, payload: dict) -> dict:
        profile = await self.employee_repository.get_by_user_id(user_id)
        if not profile:
            raise NotFoundException("Employee profile not found")
        updates = {k: v for k, v in payload.items() if v is not None}
        if not updates:
            return profile
        updated = await self.employee_repository.update(profile["id"], updates)
        if not updated:
            raise NotFoundException("Employee profile not found")
        return updated

    async def list_employees(self) -> list[dict]:
        return await self.employee_repository.list_all()

    async def create_employee(self, user_id: str, name: str, department: str, manager_id: str | None = None) -> dict:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")

        existing = await self.employee_repository.get_by_user_id(user_id)
        if existing:
            raise ValidationException("Employee profile already exists for this user")

        if manager_id:
            manager = await self.employee_repository.get_by_id(manager_id)
            if not manager:
                raise ValidationException("Manager profile not found")

        return await self.employee_repository.create(
            {
                "user_id": user_id,
                "name": name,
                "department": department,
                "manager_id": manager_id,
            }
        )

    async def update_employee(self, employee_id: str, payload: dict) -> dict:
        updates = {k: v for k, v in payload.items() if v is not None}
        if not updates:
            employee = await self.employee_repository.get_by_id(employee_id)
            if not employee:
                raise NotFoundException("Employee not found")
            return employee

        if updates.get("manager_id"):
            manager = await self.employee_repository.get_by_id(updates["manager_id"])
            if not manager:
                raise ValidationException("Manager profile not found")

        updated = await self.employee_repository.update(employee_id, updates)
        if not updated:
            raise NotFoundException("Employee not found")
        return updated

    async def delete_employee(self, employee_id: str) -> bool:
        employee = await self.employee_repository.get_by_id(employee_id)
        if not employee:
            raise NotFoundException("Employee not found")
        user_id = employee["user_id"]
        deleted_employee = await self.employee_repository.delete(employee_id)
        deleted_user = await self.user_repository.delete(user_id)
        return deleted_employee and deleted_user
