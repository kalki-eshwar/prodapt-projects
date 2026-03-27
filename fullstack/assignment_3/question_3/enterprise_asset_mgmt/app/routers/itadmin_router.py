from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.database.session import get_db
from app.dependencies.rbac import CurrentUser, require_roles
from app.models.asset import Asset
from app.models.asset_assignment import AssetAssignment
from app.models.asset_request import AssetRequest
from app.schemas.assignment_schema import AssignmentCreate, AssignmentResponse
from app.schemas.request_schema import RequestResponse

router = APIRouter(prefix='/itadmin', tags=['ITAdmin'])


@router.post('/assignments', response_model=AssignmentResponse)
def assign_asset(
    assignment: AssignmentCreate,
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_roles('SUPERADMIN', 'IT_ADMIN')),
):
    asset = db.query(Asset).filter(Asset.id == assignment.asset_id).first()
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Asset not found')

    if asset.status != 'AVAILABLE':
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Asset is not available for assignment',
        )

    active_assignment = (
        db.query(AssetAssignment)
        .filter(
            AssetAssignment.asset_id == assignment.asset_id,
            AssetAssignment.returned_date.is_(None),
        )
        .first()
    )
    if active_assignment:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Asset already has an active assignment',
        )

    db_assignment = AssetAssignment(**assignment.model_dump(), assigned_date=datetime.utcnow())
    asset.status = 'ASSIGNED'
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment


@router.post('/requests/{request_id}/approve', response_model=RequestResponse)
def approve_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_roles('SUPERADMIN', 'IT_ADMIN')),
):
    req = db.query(AssetRequest).filter(AssetRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Request not found')

    req.status = 'APPROVED'
    req.approved_by = current_user.id
    db.commit()
    db.refresh(req)
    return req


@router.post('/assignments/{assignment_id}/return')
def return_asset(
    assignment_id: int,
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_roles('SUPERADMIN', 'IT_ADMIN')),
):
    assignment = db.query(AssetAssignment).filter(AssetAssignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Assignment not found')
    if assignment.returned_date is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Assignment already returned',
        )

    assignment.returned_date = datetime.utcnow()
    asset = db.query(Asset).filter(Asset.id == assignment.asset_id).first()
    if asset:
        asset.status = 'AVAILABLE'
    db.commit()
    return {'message': 'Asset returned successfully'}
