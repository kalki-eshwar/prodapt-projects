from pydantic import BaseModel


class DepartmentBase(BaseModel):
    name: str
    manager_id: int | None = None


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentOut(DepartmentBase):
    id: int

    class Config:
        orm_mode = True
