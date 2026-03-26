from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    manager_id = Column(Integer, ForeignKey("users.id"))

    users = relationship("User", back_populates="department", foreign_keys="User.department_id")
    manager = relationship("User", back_populates="managed_department", foreign_keys=[manager_id])
