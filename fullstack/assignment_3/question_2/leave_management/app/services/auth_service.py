from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.repositories.user_repo import UserRepository
from app.repositories.department_repo import DepartmentRepository
from app.schemas.user_schema import UserCreate
from fastapi import HTTPException, status
from app.core.security import verify_password, create_access_token
from app.models.user import Role

user_repo = UserRepository()
department_repo = DepartmentRepository()

class AuthService:
    def register_user(self, db: Session, user: UserCreate):
        existing_user = user_repo.get_by_email(db, user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        if user.department_id is not None:
            department = department_repo.get_by_id(db, user.department_id)
            if not department:
                raise HTTPException(status_code=400, detail="Invalid department_id")

        try:
            return user_repo.create(db, user)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Unable to register user with the provided data")

    def login_user(self, db: Session, email: str, password: str):
        user = user_repo.get_by_email(db, email)
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        access_token = create_access_token(data={"sub": user.email, "role": user.role})
        return {"access_token": access_token, "token_type": "bearer"}

    def bootstrap_admin(self, db: Session, user: UserCreate):
        admin_count = user_repo.count_by_role(db, Role.ADMIN.value)
        if admin_count > 0:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bootstrap is disabled after first admin is created")

        user.role = Role.ADMIN.value
        user.department_id = None
        return self.register_user(db, user)
