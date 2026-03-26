from collections.abc import Callable

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.core.security import decode_access_token
from app.exceptions.custom_exceptions import AuthException, AuthorizationException
from app.repositories.user_repository import UserRepository


bearer_scheme = HTTPBearer()


def get_db() -> AsyncIOMotorDatabase:
    return get_database()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> dict:
    payload = decode_access_token(credentials.credentials)
    user_id = payload.get("sub")
    if not user_id:
        raise AuthException("Invalid token payload")

    repository = UserRepository(db)
    user = await repository.get_by_id(user_id)
    if not user:
        raise AuthException("User not found")
    return user


def require_roles(*roles: str) -> Callable:
    async def role_checker(current_user: dict = Depends(get_current_user)) -> dict:
        if current_user.get("role") not in roles:
            raise AuthorizationException("Insufficient permissions")
        return current_user

    return role_checker
