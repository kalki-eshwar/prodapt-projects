from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User


class Role:
    SUPERADMIN = "SUPERADMIN"
    IT_ADMIN = "IT_ADMIN"
    MANAGER = "MANAGER"
    EMPLOYEE = "EMPLOYEE"


def get_current_user(x_user_id: int | None = Header(None), db: Session = Depends(get_db)) -> User:
    if x_user_id is None:
        raise HTTPException(status_code=401, detail="X-User-Id header is required")

    user = db.query(User).filter(User.id == x_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def require_roles(*roles):
    def wrapper(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return current_user

    return wrapper
