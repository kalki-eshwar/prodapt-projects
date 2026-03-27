from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.rbac import CurrentUser, require_roles
from app.models.asset_request import AssetRequest
from app.models.asset_assignment import AssetAssignment
from app.models.asset import Asset
from app.schemas.asset_schema import AssetResponse
from app.schemas.request_schema import RequestCreate, RequestResponse

router = APIRouter(prefix='/employee', tags=['Employee'])


@router.post('/requests', response_model=RequestResponse)
def create_request(
    req: RequestCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_roles('EMPLOYEE')),
):
    db_req = AssetRequest(employee_id=current_user.id, **req.model_dump())
    db.add(db_req)
    db.commit()
    db.refresh(db_req)
    return db_req


@router.get('/assets', response_model=list[AssetResponse])
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
