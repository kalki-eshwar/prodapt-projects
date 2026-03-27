from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.dependencies.rbac import CurrentUser, require_roles
from app.models.asset import Asset
from app.models.asset_assignment import AssetAssignment
from app.schemas.asset_schema import AssetResponse

router = APIRouter(prefix='/manager', tags=['Manager'])


@router.get('/department/assets', response_model=List[AssetResponse])
def view_department_assets(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_roles('SUPERADMIN', 'IT_ADMIN', 'MANAGER')),
):
    if current_user.role == 'SUPERADMIN':
        return db.query(Asset).all()
    if current_user.department_id is None:
        return []
    return db.query(Asset).filter(Asset.department_id == current_user.department_id).all()


@router.get('/assets')
def view_own_assets(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_roles('SUPERADMIN', 'IT_ADMIN', 'MANAGER', 'EMPLOYEE')),
):
    assignments = (
        db.query(AssetAssignment)
        .filter(AssetAssignment.user_id == current_user.id, AssetAssignment.returned_date.is_(None))
        .all()
    )
    asset_ids = [assignment.asset_id for assignment in assignments]
    if not asset_ids:
        return []
    return db.query(Asset).filter(Asset.id.in_(asset_ids)).all()
