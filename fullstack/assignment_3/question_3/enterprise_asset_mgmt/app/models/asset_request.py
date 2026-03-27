from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.base import Base
class AssetRequest(Base):
    __tablename__ = 'asset_requests'
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('users.id'))
    asset_type = Column(String)
    reason = Column(String)
    status = Column(String, default='PENDING')
    approved_by = Column(Integer, ForeignKey('users.id'), nullable=True)