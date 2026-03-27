from pydantic import BaseModel, ConfigDict


class RequestCreate(BaseModel):
    asset_type: str
    reason: str


class RequestResponse(BaseModel):
    id: int
    employee_id: int
    asset_type: str
    reason: str
    status: str
    approved_by: int | None = None
    model_config = ConfigDict(from_attributes=True)
