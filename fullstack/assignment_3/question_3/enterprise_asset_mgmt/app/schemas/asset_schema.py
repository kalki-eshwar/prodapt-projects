from pydantic import BaseModel
from datetime import date
from typing import Optional


class AssetBase(BaseModel):
    asset_tag: str
    asset_type: str
    brand: Optional[str] = None
    model: Optional[str] = None
    purchase_date: Optional[date] = None
    status: Optional[str] = "AVAILABLE"
    department_id: Optional[int] = None


class AssetCreate(AssetBase):
    pass


class AssetOut(AssetBase):
    id: int

    class Config:
        orm_mode = True
