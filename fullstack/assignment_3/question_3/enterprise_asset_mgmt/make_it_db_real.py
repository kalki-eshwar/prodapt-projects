import os

base_dir = r"c:\Users\Administrator\Documents\Assignments\prodapt-projects\fullstack\assignment_3\question_3\enterprise_asset_mgmt"

files = {
    "app/schemas/asset_schema.py": """from pydantic import BaseModel, ConfigDict
from typing import Optional

class AssetBase(BaseModel):
    asset_tag: str
    asset_type: str
    brand: str
    model: str
    department_id: Optional[int] = None

class AssetCreate(AssetBase):
    pass

class AssetResponse(AssetBase):
    id: int
    status: str
    model_config = ConfigDict(from_attributes=True)
""",
    
    "app/schemas/request_schema.py": """from pydantic import BaseModel
class RequestCreate(BaseModel):
    asset_type: str
    reason: str
""",

    "app/schemas/assignment_schema.py": """from pydantic import BaseModel
class AssignmentCreate(BaseModel):
    asset_id: int
    user_id: int
""",

    "app/routers/superadmin_router.py": """from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.asset import Asset
from app.schemas.asset_schema import AssetCreate, AssetResponse

router = APIRouter(prefix='/superadmin', tags=['SuperAdmin'])

@router.post('/assets', response_model=AssetResponse)
def create_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    db_asset = Asset(**asset.model_dump())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.get('/assets', response_model=List[AssetResponse])
def get_all_assets(db: Session = Depends(get_db)):
    assets = db.query(Asset).all()
    return assets
""",

    "app/routers/itadmin_router.py": """from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.database.session import get_db
from app.models.asset import Asset
from app.models.asset_assignment import AssetAssignment
from app.models.asset_request import AssetRequest
from app.schemas.assignment_schema import AssignmentCreate

router = APIRouter(prefix='/itadmin', tags=['ITAdmin'])

@router.post('/assignments')
def assign_asset(assignment: AssignmentCreate, db: Session = Depends(get_db)):
    db_assignment = AssetAssignment(**assignment.model_dump(), assigned_date=datetime.utcnow())
    asset = db.query(Asset).filter(Asset.id == assignment.asset_id).first()
    if asset:
        asset.status = "ASSIGNED"
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.post('/requests/{request_id}/approve')
def approve_request(request_id: int, db: Session = Depends(get_db)):
    req = db.query(AssetRequest).filter(AssetRequest.id == request_id).first()
    if req:
        req.status = "APPROVED"
        req.approved_by = 2
        db.commit()
        db.refresh(req)
    return req

@router.post('/assignments/{assignment_id}/return')
def return_asset(assignment_id: int, db: Session = Depends(get_db)):
    assignment = db.query(AssetAssignment).filter(AssetAssignment.id == assignment_id).first()
    if assignment:
        assignment.returned_date = datetime.utcnow()
        asset = db.query(Asset).filter(Asset.id == assignment.asset_id).first()
        if asset:
            asset.status = "AVAILABLE"
        db.commit()
    return {"message": "Asset returned successfully"}
""",

    "app/routers/manager_router.py": """from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.asset import Asset
from app.schemas.asset_schema import AssetResponse

router = APIRouter(prefix='/manager', tags=['Manager'])

@router.get('/department/assets', response_model=List[AssetResponse])
def view_department_assets(db: Session = Depends(get_db)):
    # Currently hardcoded to get assets from department #1 for logic
    assets = db.query(Asset).filter(Asset.department_id == 1).all()
    return assets

@router.get('/assets')
def view_own_assets(db: Session = Depends(get_db)):
    return []
""",

    "app/routers/employee_router.py": """from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.asset_request import AssetRequest
from app.models.asset_assignment import AssetAssignment
from app.schemas.request_schema import RequestCreate

router = APIRouter(prefix='/employee', tags=['Employee'])

@router.post('/requests')
def create_request(req: RequestCreate, db: Session = Depends(get_db)):
    db_req = AssetRequest(employee_id=1, **req.model_dump())
    db.add(db_req)
    db.commit()
    db.refresh(db_req)
    return db_req

@router.get('/assets')
def view_own_assets(db: Session = Depends(get_db)):
    assignments = db.query(AssetAssignment).filter(AssetAssignment.user_id == 1).all()
    return assignments
"""
}

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Updated routers with DB interaction!")
