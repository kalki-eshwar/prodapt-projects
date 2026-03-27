from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies.rbac import require_roles, Role
from app.models.department import Department
from app.schemas.department_schema import DepartmentCreate, DepartmentOut

router = APIRouter(prefix="/superadmin", tags=["superadmin"])


@router.post("/departments", response_model=DepartmentOut, dependencies=[Depends(require_roles(Role.SUPERADMIN))])
def create_department(dept: DepartmentCreate, db: Session = Depends(get_db)):
    existing = db.query(Department).filter(Department.name == dept.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Department already exists")
    department = Department(name=dept.name, manager_id=dept.manager_id)
    db.add(department)
    db.commit()
    db.refresh(department)
    return department
