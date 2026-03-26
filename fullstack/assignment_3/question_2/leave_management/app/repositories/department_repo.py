from sqlalchemy.orm import Session
from app.models.department import Department
from app.schemas.department_schema import DepartmentCreate

class DepartmentRepository:
    def get_by_name(self, db: Session, name: str):
        return db.query(Department).filter(Department.name == name).first()

    def get_by_id(self, db: Session, dept_id: int):
        return db.query(Department).filter(Department.id == dept_id).first()

    def create(self, db: Session, dept: DepartmentCreate):
        db_dept = Department(name=dept.name, manager_id=dept.manager_id)
        db.add(db_dept)
        db.commit()
        db.refresh(db_dept)
        return db_dept

    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Department).offset(skip).limit(limit).all()
