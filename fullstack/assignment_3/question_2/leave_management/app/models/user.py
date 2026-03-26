from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.database.base import Base

class Role(str, PyEnum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    EMPLOYEE = "EMPLOYEE"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default=Role.EMPLOYEE.value)
    department_id = Column(Integer, ForeignKey("departments.id"))

    department = relationship("Department", back_populates="users", foreign_keys=[department_id])
    managed_department = relationship("Department", back_populates="manager", uselist=False, foreign_keys="Department.manager_id")
    leaves = relationship("LeaveRequest", back_populates="employee", foreign_keys="LeaveRequest.employee_id")
