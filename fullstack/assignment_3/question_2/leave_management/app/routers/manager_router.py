from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.leave_schema import LeaveRequestResponse, LeaveStatus
from app.services.leave_service import LeaveService
from app.dependencies.rbac import require_role
from app.models.user import User, Role

router = APIRouter(prefix="/manager", tags=["Manager"])
leave_service = LeaveService()

@router.get("/leaves")
def get_department_leaves(page: int = 1, size: int = 10, db: Session = Depends(get_db), current_user: User = Depends(require_role([Role.MANAGER]))):
    return leave_service.get_department_leaves(db, current_user, page, size)

@router.put("/leave/{leave_id}/status", response_model=LeaveRequestResponse)
def evaluate_leave(leave_id: int, status: LeaveStatus, db: Session = Depends(get_db), current_user: User = Depends(require_role([Role.MANAGER]))):
    return leave_service.update_leave_status(db, leave_id, status, current_user)
