from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies.rbac import require_roles, Role, get_current_user
from app.models.asset import Asset
from app.models.asset_request import AssetRequest
from app.models.asset_assignment import AssetAssignment
from app.schemas.request_schema import RequestCreate, RequestOut
from app.schemas.asset_schema import AssetOut
from app.models.user import User

router = APIRouter(prefix="/employee", tags=["employee"])


@router.post("/requests", response_model=RequestOut, dependencies=[Depends(require_roles(Role.EMPLOYEE))])
def request_asset(request: RequestCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.id != request.employee_id:
        raise HTTPException(status_code=403, detail="Cannot create request for another employee")

    new_request = AssetRequest(
        employee_id=request.employee_id,
        asset_type=request.asset_type,
        reason=request.reason,
        status="PENDING",
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request


@router.get("/my-assets", response_model=list[AssetOut], dependencies=[Depends(require_roles(Role.EMPLOYEE, Role.MANAGER, Role.IT_ADMIN, Role.SUPERADMIN))])
def view_my_assets(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    assignments = db.query(AssetAssignment).filter(AssetAssignment.user_id == current_user.id, AssetAssignment.returned_date == None).all()
    asset_ids = [a.asset_id for a in assignments]
    return db.query(Asset).filter(Asset.id.in_(asset_ids)).all()
