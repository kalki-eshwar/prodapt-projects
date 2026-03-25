from datetime import datetime, timezone

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class EmployeeRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["employees"]

    @staticmethod
    def _serialize(document: dict | None) -> dict | None:
        if not document:
            return None
        document["id"] = str(document.pop("_id"))
        document["user_id"] = str(document["user_id"])
        if document.get("manager_id"):
            document["manager_id"] = str(document["manager_id"])
        return document

    async def create(self, data: dict) -> dict:
        payload = {
            **data,
            "user_id": ObjectId(data["user_id"]),
            "manager_id": ObjectId(data["manager_id"]) if data.get("manager_id") else None,
            "created_at": datetime.now(timezone.utc),
        }
        result = await self.collection.insert_one(payload)
        created = await self.collection.find_one({"_id": result.inserted_id})
        return self._serialize(created)

    async def get_by_id(self, employee_id: str) -> dict | None:
        if not ObjectId.is_valid(employee_id):
            return None
        found = await self.collection.find_one({"_id": ObjectId(employee_id)})
        return self._serialize(found)

    async def get_by_user_id(self, user_id: str) -> dict | None:
        if not ObjectId.is_valid(user_id):
            return None
        found = await self.collection.find_one({"user_id": ObjectId(user_id)})
        return self._serialize(found)

    async def list_all(self) -> list[dict]:
        items: list[dict] = []
        cursor = self.collection.find().sort("created_at", -1)
        async for doc in cursor:
            items.append(self._serialize(doc))
        return items

    async def update(self, employee_id: str, data: dict) -> dict | None:
        if not ObjectId.is_valid(employee_id):
            return None
        payload = {**data}
        if "manager_id" in payload:
            payload["manager_id"] = ObjectId(payload["manager_id"]) if payload["manager_id"] else None
        await self.collection.update_one({"_id": ObjectId(employee_id)}, {"$set": payload})
        found = await self.collection.find_one({"_id": ObjectId(employee_id)})
        return self._serialize(found)

    async def delete(self, employee_id: str) -> bool:
        if not ObjectId.is_valid(employee_id):
            return False
        result = await self.collection.delete_one({"_id": ObjectId(employee_id)})
        return result.deleted_count == 1
