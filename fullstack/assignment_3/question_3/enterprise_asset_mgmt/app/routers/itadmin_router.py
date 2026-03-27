from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies.rbac import require_roles, Role, get_current_user
from app.models.asset import Asset
from app.models.asset_assignment import AssetAssignment
from app.models.asset_request import AssetRequest
from app.schemas.asset_schema import AssetCreate, AssetOut
from app.schemas.assignment_schema import AssignmentCreate, AssignmentOut, AssignmentUpdate
from app.schemas.request_schema import RequestUpdate

router = APIRouter(prefix="/itadmin", tags=["itadmin"])


@router.post("/assets", response_model=AssetOut, dependencies=[Depends(require_roles(Role.SUPERADMIN, Role.IT_ADMIN))])
def create_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    existing = db.query(Asset).filter(Asset.asset_tag == asset.asset_tag).first()
    if existing:
        raise HTTPException(status_code=400, detail="Asset tag already exists")
    item = Asset(
        asset_tag=asset.asset_tag,
        asset_type=asset.asset_type,
        brand=asset.brand,
        model=asset.model,
        purchase_date=asset.purchase_date,
        status=asset.status or "AVAILABLE",
        department_id=asset.department_id,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.post("/assignments", response_model=AssignmentOut, dependencies=[Depends(require_roles(Role.SUPERADMIN, Role.IT_ADMIN))])
def assign_asset(data: AssignmentCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    asset = db.query(Asset).filter(Asset.id == data.asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    if asset.status != "AVAILABLE":
        raise HTTPException(status_code=400, detail="Asset is not available")

    active_assignment = db.query(AssetAssignment).filter(AssetAssignment.asset_id == asset.id, AssetAssignment.returned_date == None).first()
    if active_assignment:
        raise HTTPException(status_code=400, detail="Asset is already assigned")

    assignment = AssetAssignment(
        asset_id=asset.id,
        user_id=data.user_id,
        assigned_date=data.assigned_date,
    )
    asset.status = "ASSIGNED"
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment


@router.patch("/assignments/{assignment_id}", response_model=AssignmentOut, dependencies=[Depends(require_roles(Role.SUPERADMIN, Role.IT_ADMIN))])
def return_assignment(assignment_id: int, payload: AssignmentUpdate, db: Session = Depends(get_db)):
    assignment = db.query(AssetAssignment).filter(AssetAssignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    if assignment.returned_date is not None:
        raise HTTPException(status_code=400, detail="Already returned")

    assignment.returned_date = payload.returned_date or date.today()
    assignment.condition_on_return = payload.condition_on_return
    asset = db.query(Asset).filter(Asset.id == assignment.asset_id).first()
    if asset:
        asset.status = "AVAILABLE"

    db.commit()
    db.refresh(assignment)
    return assignment


@router.post("/requests/{request_id}/approve", dependencies=[Depends(require_roles(Role.SUPERADMIN, Role.IT_ADMIN))])
def approve_request(request_id: int, payload: RequestUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    request_row = db.query(AssetRequest).filter(AssetRequest.id == request_id).first()
    if not request_row:
        raise HTTPException(status_code=404, detail="Request not found")
    if request_row.status != "PENDING":
        raise HTTPException(status_code=400, detail="Request not pending")

    request_row.status = payload.status
    request_row.approved_by = current_user.id

    if payload.status == "APPROVED":
        asset = db.query(Asset).filter(Asset.asset_type == request_row.asset_type, Asset.status == "AVAILABLE").first()
        if not asset:
            raise HTTPException(status_code=400, detail="No available asset of requested type")

        assignment = AssetAssignment(asset_id=asset.id, user_id=request_row.employee_id, assigned_date=date.today())
        asset.status = "ASSIGNED"
        db.add(assignment)

    db.commit()
    return {"request_id": request_row.id, "status": request_row.status, "approved_by": request_row.approved_by}
