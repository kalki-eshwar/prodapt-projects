from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.database import (
    get_database,
    initialize_database,
    ping_database,
    switch_to_mock_database,
)
from app.exceptions.exception_handlers import register_exception_handlers
from app.middleware.logging import LoggingMiddleware
from app.middleware.cors import add_cors_middleware


@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.app_env != "test":
        db_ready = await ping_database()
        if not db_ready:
            if settings.app_env == "development":
                switch_to_mock_database()
            else:
                raise RuntimeError(
                    f"MongoDB is not reachable at {settings.mongo_uri}. Start MongoDB and retry."
                )
        await initialize_database(get_database())
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.add_middleware(LoggingMiddleware)
register_exception_handlers(app)
app.include_router(api_router)
add_cors_middleware(app)

@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    db_ready = await ping_database()
    return {
        "status": "ok" if db_ready else "degraded",
        "database": "ok" if db_ready else "down",
    }
