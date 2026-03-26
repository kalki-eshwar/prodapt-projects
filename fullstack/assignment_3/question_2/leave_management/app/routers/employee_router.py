from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.leave_schema import LeaveRequestCreate, LeaveRequestResponse
from app.services.leave_service import LeaveService
from app.dependencies.rbac import get_current_user, require_role
from app.models.user import User, Role

router = APIRouter(prefix="/employee", tags=["Employee"])
leave_service = LeaveService()

@router.post("/leave", response_model=LeaveRequestResponse)
def apply_leave(data: LeaveRequestCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role([Role.EMPLOYEE, Role.MANAGER, Role.ADMIN]))):
    return leave_service.apply_leave(db, current_user.id, data)

@router.get("/leaves")
def get_my_leaves(page: int = 1, size: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return leave_service.get_employee_leaves(db, current_user.id, page, size)
