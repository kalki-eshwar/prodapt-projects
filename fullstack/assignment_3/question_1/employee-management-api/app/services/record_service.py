from datetime import date, datetime, time, timezone

from bson import ObjectId

from app.exceptions.custom_exceptions import NotFoundException, ValidationException
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.record_repository import RecordRepository


class RecordService:
    def __init__(self, record_repository: RecordRepository, employee_repository: EmployeeRepository):
        self.record_repository = record_repository
        self.employee_repository = employee_repository

    async def create_record(self, user_id: str, payload: dict) -> dict:
        employee = await self.employee_repository.get_by_user_id(user_id)
        if not employee:
            raise NotFoundException("Employee profile not found")

        record_type = payload["type"]
        status = "approved" if record_type == "attendance" else "pending"

        data = {
            "employee_id": employee["id"],
            "type": record_type,
            "date": payload.get("date"),
            "from_date": payload.get("from_date"),
            "to_date": payload.get("to_date"),
            "status": status,
        }
        return await self.record_repository.create(data)

    async def get_my_records(self, user_id: str) -> list[dict]:
        employee = await self.employee_repository.get_by_user_id(user_id)
        if not employee:
            raise NotFoundException("Employee profile not found")
        return await self.record_repository.list_by_employee(employee["id"])

    async def list_records(self, filters: dict) -> list[dict]:
        query: dict = {}
        if filters.get("employee_id") and ObjectId.is_valid(filters["employee_id"]):
            query["employee_id"] = ObjectId(filters["employee_id"])
        if filters.get("type"):
            query["type"] = filters["type"]
        if filters.get("status"):
            query["status"] = filters["status"]

        date_range = self._build_date_range(filters)
        if date_range:
            query["$or"] = [
                {"date": date_range},
                {"from_date": date_range},
                {"to_date": date_range},
            ]

        return await self.record_repository.list_all(query)

    @staticmethod
    def _build_date_range(filters: dict) -> dict | None:
        from_date: date | None = filters.get("from_date")
        to_date: date | None = filters.get("to_date")
        if not from_date and not to_date:
            return None
        if from_date and to_date and from_date > to_date:
            raise ValidationException("from_date cannot be after to_date")

        date_query: dict = {}
        if from_date:
            date_query["$gte"] = datetime.combine(from_date, time.min, tzinfo=timezone.utc)
        if to_date:
            date_query["$lte"] = datetime.combine(to_date, time.max, tzinfo=timezone.utc)
        return date_query

    async def approve_leave(self, record_id: str) -> dict:
        record = await self.record_repository.get_by_id(record_id)
        if not record:
            raise NotFoundException("Record not found")
        if record["type"] != "leave":
            raise ValidationException("Only leave records can be approved")
        if record["status"] != "pending":
            raise ValidationException("Only pending leaves can be approved")
        return await self.record_repository.update_status(record_id, "approved")

    async def reject_leave(self, record_id: str) -> dict:
        record = await self.record_repository.get_by_id(record_id)
        if not record:
            raise NotFoundException("Record not found")
        if record["type"] != "leave":
            raise ValidationException("Only leave records can be rejected")
        if record["status"] != "pending":
            raise ValidationException("Only pending leaves can be rejected")
        return await self.record_repository.update_status(record_id, "rejected")

    async def report_summary(self) -> dict:
        all_records = await self.record_repository.list_all({})
        return {
            "total_records": len(all_records),
            "pending_leaves": len([r for r in all_records if r["type"] == "leave" and r["status"] == "pending"]),
            "approved_leaves": len([r for r in all_records if r["type"] == "leave" and r["status"] == "approved"]),
            "rejected_leaves": len([r for r in all_records if r["type"] == "leave" and r["status"] == "rejected"]),
            "attendance_entries": len([r for r in all_records if r["type"] == "attendance"]),
        }
