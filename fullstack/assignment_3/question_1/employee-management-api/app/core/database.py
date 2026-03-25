import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings


logger = logging.getLogger("employee-management-api")
client = AsyncIOMotorClient(settings.mongo_uri)


def get_database() -> AsyncIOMotorDatabase:
    return client[settings.mongo_db]


async def ping_database() -> bool:
    try:
        await client.admin.command("ping")
        return True
    except Exception as exc:  # pragma: no cover - defensive runtime guard
        logger.error("MongoDB ping failed: %s", exc)
        return False


async def initialize_database(db: AsyncIOMotorDatabase) -> None:
    await db["users"].create_index("email", unique=True)
    await db["employees"].create_index("user_id", unique=True)
    await db["employees"].create_index("manager_id")
    await db["records"].create_index("employee_id")
    await db["records"].create_index([("type", 1), ("status", 1)])
    await db["records"].create_index("date")
    await db["records"].create_index([("from_date", 1), ("to_date", 1)])
