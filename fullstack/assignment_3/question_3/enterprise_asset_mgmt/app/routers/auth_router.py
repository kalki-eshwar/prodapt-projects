from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserOut, UserLogin

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
def register_user(data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(name=data.name, email=data.email, password=data.password, role=data.role, department_id=data.department_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login")
def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email, User.password == credentials.password).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # For simplicity we issue a transparent user id
    return {"user_id": user.id, "role": user.role}
