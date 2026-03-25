from datetime import date, datetime, time, timezone

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class RecordRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["records"]

    @staticmethod
    def _serialize(document: dict | None) -> dict | None:
        if not document:
            return None
        document["id"] = str(document.pop("_id"))
        document["employee_id"] = str(document["employee_id"])
        for field in ("date", "from_date", "to_date"):
            value = document.get(field)
            if isinstance(value, datetime):
                document[field] = value.date()
        return document

    @staticmethod
    def _to_datetime(value: date | None) -> datetime | None:
        if value is None:
            return None
        return datetime.combine(value, time.min, tzinfo=timezone.utc)

    async def create(self, data: dict) -> dict:
        payload = {
            **data,
            "employee_id": ObjectId(data["employee_id"]),
            "date": self._to_datetime(data.get("date")),
            "from_date": self._to_datetime(data.get("from_date")),
            "to_date": self._to_datetime(data.get("to_date")),
            "created_at": datetime.now(timezone.utc),
        }
        result = await self.collection.insert_one(payload)
        created = await self.collection.find_one({"_id": result.inserted_id})
        return self._serialize(created)

    async def get_by_id(self, record_id: str) -> dict | None:
        if not ObjectId.is_valid(record_id):
            return None
        found = await self.collection.find_one({"_id": ObjectId(record_id)})
        return self._serialize(found)

    async def list_by_employee(self, employee_id: str) -> list[dict]:
        if not ObjectId.is_valid(employee_id):
            return []
        items: list[dict] = []
        cursor = self.collection.find({"employee_id": ObjectId(employee_id)}).sort("created_at", -1)
        async for doc in cursor:
            items.append(self._serialize(doc))
        return items

    async def list_all(self, filters: dict | None = None) -> list[dict]:
        query: dict = filters or {}
        items: list[dict] = []
        cursor = self.collection.find(query).sort("created_at", -1)
        async for doc in cursor:
            items.append(self._serialize(doc))
        return items

    async def update_status(self, record_id: str, status: str) -> dict | None:
        if not ObjectId.is_valid(record_id):
            return None
        await self.collection.update_one({"_id": ObjectId(record_id)}, {"$set": {"status": status}})
        found = await self.collection.find_one({"_id": ObjectId(record_id)})
        return self._serialize(found)
