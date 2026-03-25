from datetime import datetime

from pydantic import BaseModel, EmailStr


class EmployeeBase(BaseModel):
    name: str
    department: str
    manager_id: str | None = None


class EmployeeCreateByAdminRequest(EmployeeBase):
    email: EmailStr
    password: str
    role: str = "employee"


class EmployeeCreateRequest(EmployeeBase):
    user_id: str


class EmployeeUpdateMeRequest(BaseModel):
    name: str | None = None
    department: str | None = None


class EmployeeUpdateByAdminRequest(BaseModel):
    name: str | None = None
    department: str | None = None
    manager_id: str | None = None


class EmployeeResponse(BaseModel):
    id: str
    user_id: str
    name: str
    department: str
    manager_id: str | None = None
    created_at: datetime | None = None
