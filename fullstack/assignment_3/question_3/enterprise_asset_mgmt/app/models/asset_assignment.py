from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.database.base import Base
class AssetAssignment(Base):
    __tablename__ = 'asset_assignments'
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey('assets.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    assigned_date = Column(DateTime)
    returned_date = Column(DateTime, nullable=True)
    condition_on_return = Column(String, nullable=True)