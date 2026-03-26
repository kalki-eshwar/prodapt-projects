from sqlalchemy.orm import Session
from app.repositories.leave_repo import LeaveRepository
from app.schemas.leave_schema import LeaveRequestCreate, LeaveStatus
from app.models.user import User, Role
from fastapi import HTTPException
from datetime import date
from math import ceil
from app.core.pagination import PaginatedResponse
from app.schemas.leave_schema import LeaveRequestResponse

leave_repo = LeaveRepository()

class LeaveService:
    def apply_leave(self, db: Session, employee_id: int, data: LeaveRequestCreate):
        if data.start_date < date.today():
            raise HTTPException(status_code=400, detail="Start date cannot be in the past")
        if data.start_date > data.end_date:
            raise HTTPException(status_code=400, detail="End date must be after start date")
        
        overlap = leave_repo.check_overlap(db, employee_id, data.start_date, data.end_date)
        if overlap:
            raise HTTPException(status_code=400, detail="Leave requested overlaps with existing leave")
            
        return leave_repo.create(db, employee_id, data)

    def get_employee_leaves(self, db: Session, employee_id: int, page: int = 1, size: int = 10):
        skip = (page - 1) * size
        items = leave_repo.get_by_employee(db, employee_id, skip, size)
        total = leave_repo.count_by_employee(db, employee_id)
        return PaginatedResponse[LeaveRequestResponse](items=items, total=total, page=page, size=size, pages=ceil(total/size))

    def get_department_leaves(self, db: Session, manager: User, page: int = 1, size: int = 10):
        if not manager.managed_department:
            raise HTTPException(status_code=400, detail="Manager is not assigned to a department")
        
        skip = (page - 1) * size
        items = leave_repo.get_by_department(db, manager.managed_department.id, skip, size)
        total = leave_repo.count_by_department(db, manager.managed_department.id)
        return PaginatedResponse[LeaveRequestResponse](items=items, total=total, page=page, size=size, pages=ceil(total/size))

    def get_all_leaves(self, db: Session, page: int = 1, size: int = 10):
        skip = (page - 1) * size
        items = leave_repo.get_all(db, skip, size)
        total = leave_repo.count_all(db)
        return PaginatedResponse[LeaveRequestResponse](items=items, total=total, page=page, size=size, pages=ceil(total/size))

    def update_leave_status(self, db: Session, leave_id: int, status: LeaveStatus, approver: User):
        leave = leave_repo.get_by_id(db, leave_id)
        if not leave:
            raise HTTPException(status_code=404, detail="Leave request not found")
        
        # Manager can only approve their own department's leaves
        if approver.role == Role.MANAGER:
            if leave.employee.department_id != approver.managed_department.id:
                 raise HTTPException(status_code=403, detail="Cannot approve leave for another department")
            if leave.status != LeaveStatus.PENDING:
                raise HTTPException(status_code=400, detail="Can only approve/reject pending leaves")
        
        updated_leave = leave_repo.update_status(db, leave_id, status.value, approver.id)
        return updated_leave
