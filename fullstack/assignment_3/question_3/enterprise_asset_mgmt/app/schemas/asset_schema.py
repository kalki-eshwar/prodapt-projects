from pydantic import BaseModel, ConfigDict
from typing import Optional

class AssetBase(BaseModel):
    asset_tag: str
    asset_type: str
    brand: str
    model: str
    department_id: Optional[int] = None

class AssetCreate(AssetBase):
    pass

class AssetResponse(AssetBase):
    id: int
    status: str
    model_config = ConfigDict(from_attributes=True)
