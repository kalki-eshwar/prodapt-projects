from datetime import datetime, timezone

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class UserRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["users"]

    @staticmethod
    def _serialize(document: dict | None) -> dict | None:
        if not document:
            return None
        document["id"] = str(document.pop("_id"))
        return document

    async def create(self, data: dict) -> dict:
        payload = {**data, "created_at": datetime.now(timezone.utc)}
        result = await self.collection.insert_one(payload)
        created = await self.collection.find_one({"_id": result.inserted_id})
        return self._serialize(created)

    async def get_by_email(self, email: str) -> dict | None:
        found = await self.collection.find_one({"email": email})
        return self._serialize(found)

    async def get_by_id(self, user_id: str) -> dict | None:
        if not ObjectId.is_valid(user_id):
            return None
        found = await self.collection.find_one({"_id": ObjectId(user_id)})
        return self._serialize(found)

    async def delete(self, user_id: str) -> bool:
        if not ObjectId.is_valid(user_id):
            return False
        result = await self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count == 1
