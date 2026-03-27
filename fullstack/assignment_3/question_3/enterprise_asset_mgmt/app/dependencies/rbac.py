from typing import Optional

from fastapi import Depends, Header, HTTPException, status
from pydantic import BaseModel


class CurrentUser(BaseModel):
    id: int
    role: str
    department_id: Optional[int] = None


def get_current_user(
    x_user_id: int = Header(default=1),
    x_role: str = Header(default="EMPLOYEE"),
    x_department_id: Optional[int] = Header(default=None),
) -> CurrentUser:
    return CurrentUser(
        id=x_user_id,
        role=x_role.upper(),
        department_id=x_department_id,
    )


def require_roles(*roles: str):
    allowed_roles = {role.upper() for role in roles}

    def wrapper(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return wrapper