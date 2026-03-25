from datetime import date as date_type
from datetime import datetime

from pydantic import BaseModel, model_validator


class RecordCreateRequest(BaseModel):
    type: str
    date: date_type | None = None
    from_date: date_type | None = None
    to_date: date_type | None = None

    @model_validator(mode="after")
    def validate_by_type(self):
        if self.type not in {"attendance", "leave"}:
            raise ValueError("type must be attendance or leave")

        if self.type == "attendance" and not self.date:
            raise ValueError("date is required for attendance")

        if self.type == "leave":
            if not self.from_date or not self.to_date:
                raise ValueError("from_date and to_date are required for leave")
            if self.from_date > self.to_date:
                raise ValueError("from_date cannot be after to_date")

        return self


class RecordResponse(BaseModel):
    id: str
    employee_id: str
    type: str
    date: date_type | None = None
    from_date: date_type | None = None
    to_date: date_type | None = None
    status: str
    created_at: datetime | None = None


class RecordQueryParams(BaseModel):
    employee_id: str | None = None
    type: str | None = None
    status: str | None = None
    from_date: date_type | None = None
    to_date: date_type | None = None
