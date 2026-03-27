from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AssignmentCreate(BaseModel):
    asset_id: int
    user_id: int


class AssignmentResponse(BaseModel):
    id: int
    asset_id: int
    user_id: int
    assigned_date: datetime
    returned_date: datetime | None = None
    condition_on_return: str | None = None
    model_config = ConfigDict(from_attributes=True)
