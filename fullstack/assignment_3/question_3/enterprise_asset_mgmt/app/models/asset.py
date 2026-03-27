from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.database.base import Base
class Asset(Base):
    __tablename__ = 'assets'
    id = Column(Integer, primary_key=True, index=True)
    asset_tag = Column(String, unique=True, index=True)
    asset_type = Column(String)
    brand = Column(String)
    model = Column(String)
    status = Column(String, default='AVAILABLE')
    department_id = Column(Integer, ForeignKey('departments.id'))