from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies.rbac import require_roles, Role, get_current_user
from app.models.asset import Asset
from app.models.asset_assignment import AssetAssignment
from app.models.user import User
from app.schemas.asset_schema import AssetOut

router = APIRouter(prefix="/manager", tags=["manager"])


@router.get("/department-assets", response_model=list[AssetOut], dependencies=[Depends(require_roles(Role.SUPERADMIN, Role.IT_ADMIN, Role.MANAGER))])
def get_department_assets(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role == Role.MANAGER and current_user.department_id is not None:
        return db.query(Asset).filter(Asset.department_id == current_user.department_id).all()

    return db.query(Asset).all()


@router.get("/my-assets", response_model=list[AssetOut], dependencies=[Depends(require_roles(Role.SUPERADMIN, Role.IT_ADMIN, Role.MANAGER, Role.EMPLOYEE))])
def get_my_assets(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return (
        db.query(Asset)
        .join(AssetAssignment)
        .filter(AssetAssignment.user_id == current_user.id, AssetAssignment.returned_date == None)
        .all()
    )
