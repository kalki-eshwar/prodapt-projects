import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from mongomock_motor import AsyncMongoMockClient

from app.core.config import settings


logger = logging.getLogger("employee-management-api")
client = AsyncIOMotorClient(settings.mongo_uri)
_using_mock_database = False


def switch_to_mock_database() -> None:
    global client, _using_mock_database
    if _using_mock_database:
        return
    client = AsyncMongoMockClient()
    _using_mock_database = True
    logger.warning("Using in-memory MongoDB fallback (mongomock)")


def is_using_mock_database() -> bool:
    return _using_mock_database


def get_database() -> AsyncIOMotorDatabase:
    return client[settings.mongo_db]


async def ping_database() -> bool:
    if _using_mock_database:
        return True
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
