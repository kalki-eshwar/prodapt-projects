from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    asset_tag = Column(String, nullable=False, unique=True, index=True)
    asset_type = Column(String, nullable=False)
    brand = Column(String)
    model = Column(String)
    purchase_date = Column(Date)
    status = Column(String, nullable=False, default="AVAILABLE")
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)

    department = relationship("Department", back_populates="assets")
    assignments = relationship("AssetAssignment", back_populates="asset")
