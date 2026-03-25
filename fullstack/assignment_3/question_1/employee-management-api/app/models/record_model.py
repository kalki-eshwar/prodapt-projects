from datetime import date, datetime

from pydantic import BaseModel


class RecordModel(BaseModel):
    id: str | None = None
    employee_id: str
    type: str
    date: date | None = None
    from_date: date | None = None
    to_date: date | None = None
    status: str = "pending"
    created_at: datetime | None = None
