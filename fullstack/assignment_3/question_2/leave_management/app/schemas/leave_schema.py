from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum

class LeaveStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class LeaveRequestBase(BaseModel):
    start_date: date
    end_date: date
    reason: str

class LeaveRequestCreate(LeaveRequestBase):
    pass

class LeaveRequestResponse(LeaveRequestBase):
    id: int
    employee_id: int
    status: LeaveStatus
    approved_by: Optional[int] = None

    class Config:
        from_attributes = True
