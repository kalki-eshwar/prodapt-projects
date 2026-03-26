from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.core.security import get_password_hash

class UserRepository:
    def get_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def get_by_id(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    def create(self, db: Session, user: UserCreate):
        hashed_password = get_password_hash(user.password)
        db_user = User(
            name=user.name,
            email=user.email,
            password=hashed_password,
            role=user.role,
            department_id=user.department_id
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()

    def update_role(self, db: Session, user: User, role: str):
        user.role = role
        db.commit()
        db.refresh(user)
        return user

    def count_all(self, db: Session):
        return db.query(User).count()

    def count_by_role(self, db: Session, role: str):
        return db.query(User).filter(User.role == role).count()
