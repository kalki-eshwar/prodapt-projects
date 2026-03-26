from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.leave_schema import LeaveRequestResponse, LeaveStatus
from app.schemas.department_schema import DepartmentCreate, DepartmentResponse
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.leave_service import LeaveService
from app.repositories.department_repo import DepartmentRepository
from app.services.auth_service import AuthService
from app.dependencies.rbac import require_role
from app.models.user import User, Role

router = APIRouter(prefix="/admin", tags=["Admin"])
leave_service = LeaveService()
dept_repo = DepartmentRepository()
auth_service = AuthService()

@router.get("/leaves")
def get_all_leaves(page: int = 1, size: int = 10, db: Session = Depends(get_db), current_user: User = Depends(require_role([Role.ADMIN]))):
    return leave_service.get_all_leaves(db, page, size)

@router.put("/leave/{leave_id}/status", response_model=LeaveRequestResponse)
def override_leave_status(leave_id: int, status: LeaveStatus, db: Session = Depends(get_db), current_user: User = Depends(require_role([Role.ADMIN]))):
    return leave_service.update_leave_status(db, leave_id, status, current_user)

@router.post("/department", response_model=DepartmentResponse)
def create_department(data: DepartmentCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role([Role.ADMIN]))):
    return dept_repo.create(db, data)

@router.post("/user", response_model=UserResponse)
def create_user(data: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role([Role.ADMIN]))):
    return auth_service.register_user(db, data)
