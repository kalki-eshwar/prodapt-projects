from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.controllers.admin_controller import (
    create_employee_admin_controller,
    delete_employee_admin_controller,
    report_admin_controller,
    update_employee_admin_controller,
)
from app.core.dependencies import get_db, require_roles
from app.schemas.employee_schema import (
    EmployeeCreateByAdminRequest,
    EmployeeResponse,
    EmployeeUpdateByAdminRequest,
)


router = APIRouter()


@router.post("/employees")
async def create_employee(
    payload: EmployeeCreateByAdminRequest,
    _: dict = Depends(require_roles("admin")),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    return await create_employee_admin_controller(payload.model_dump(), db)


@router.put("/employees/{id}", response_model=EmployeeResponse)
async def update_employee(
    id: str,
    payload: EmployeeUpdateByAdminRequest,
    _: dict = Depends(require_roles("admin")),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    return await update_employee_admin_controller(id, payload.model_dump(), db)


@router.delete("/employees/{id}")
async def delete_employee(
    id: str,
    _: dict = Depends(require_roles("admin")),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    return await delete_employee_admin_controller(id, db)


@router.get("/reports")
async def get_reports(
    _: dict = Depends(require_roles("admin")),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    return await report_admin_controller(db)
