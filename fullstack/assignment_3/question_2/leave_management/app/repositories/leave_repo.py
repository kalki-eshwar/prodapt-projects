from sqlalchemy.orm import Session
from app.models.leave_request import LeaveRequest
from app.schemas.leave_schema import LeaveRequestCreate
from typing import List

class LeaveRepository:
    def create(self, db: Session, employee_id: int, leave: LeaveRequestCreate):
        db_leave = LeaveRequest(
            employee_id=employee_id,
            start_date=leave.start_date,
            end_date=leave.end_date,
            reason=leave.reason
        )
        db.add(db_leave)
        db.commit()
        db.refresh(db_leave)
        return db_leave

    def get_by_employee(self, db: Session, employee_id: int, skip: int = 0, limit: int = 100):
        return db.query(LeaveRequest).filter(LeaveRequest.employee_id == employee_id).offset(skip).limit(limit).all()

    def get_by_department(self, db: Session, department_id: int, skip: int = 0, limit: int = 100):
        from app.models.user import User
        return (
            db.query(LeaveRequest)
            .join(User, LeaveRequest.employee_id == User.id)
            .filter(User.department_id == department_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(LeaveRequest).offset(skip).limit(limit).all()

    def update_status(self, db: Session, leave_id: int, status: str, approver_id: int):
        leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
        if leave:
            leave.status = status
            leave.approved_by = approver_id
            db.commit()
            db.refresh(leave)
        return leave

    def get_by_id(self, db: Session, leave_id: int):
        return db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()

    def check_overlap(self, db: Session, employee_id: int, start_date, end_date):
        return db.query(LeaveRequest).filter(
            LeaveRequest.employee_id == employee_id,
            LeaveRequest.status != 'REJECTED',
            LeaveRequest.start_date <= end_date,
            LeaveRequest.end_date >= start_date
        ).first()

    def count_all(self, db: Session):
        return db.query(LeaveRequest).count()

    def count_by_department(self, db: Session, department_id: int):
        from app.models.user import User
        return (
            db.query(LeaveRequest)
            .join(User, LeaveRequest.employee_id == User.id)
            .filter(User.department_id == department_id)
            .count()
        )

    def count_by_employee(self, db: Session, employee_id: int):
        return db.query(LeaveRequest).filter(LeaveRequest.employee_id == employee_id).count()
