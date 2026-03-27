from pydantic import BaseModel


class RequestBase(BaseModel):
    employee_id: int
    asset_type: str
    reason: str


class RequestCreate(RequestBase):
    pass


class RequestUpdate(BaseModel):
    status: str
    approved_by: int | None = None


class RequestOut(RequestBase):
    id: int
    status: str
    approved_by: int | None

    class Config:
        orm_mode = True
