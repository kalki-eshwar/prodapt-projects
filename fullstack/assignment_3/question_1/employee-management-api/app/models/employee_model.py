from datetime import datetime

from pydantic import BaseModel


class EmployeeModel(BaseModel):
    id: str | None = None
    user_id: str
    name: str
    department: str
    manager_id: str | None = None
    created_at: datetime | None = None
