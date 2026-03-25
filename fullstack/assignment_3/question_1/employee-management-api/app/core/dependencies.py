from collections.abc import Callable

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.core.security import decode_access_token
from app.exceptions.custom_exceptions import AuthException, AuthorizationException
from app.repositories.user_repository import UserRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db() -> AsyncIOMotorDatabase:
    return get_database()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> dict:
    payload = decode_access_token(token)
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
