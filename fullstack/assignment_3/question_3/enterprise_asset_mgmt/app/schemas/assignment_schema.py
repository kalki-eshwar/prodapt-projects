from pydantic import BaseModel
from datetime import date
from typing import Optional


class AssignmentBase(BaseModel):
    asset_id: int
    user_id: int
    assigned_date: date


class AssignmentCreate(AssignmentBase):
    pass


class AssignmentUpdate(BaseModel):
    returned_date: Optional[date] = None
    condition_on_return: Optional[str] = None


class AssignmentOut(AssignmentBase):
    id: int
    returned_date: Optional[date]
    condition_on_return: Optional[str]

    class Config:
        orm_mode = True
