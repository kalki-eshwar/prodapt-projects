from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.controllers.employee_controller import (
    get_me_controller,
    list_employees_controller,
    update_me_controller,
)
from app.core.dependencies import get_current_user, get_db, require_roles
from app.schemas.employee_schema import EmployeeResponse, EmployeeUpdateMeRequest


router = APIRouter()


@router.get("/me", response_model=EmployeeResponse)
async def get_me(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    return await get_me_controller(current_user["id"], db)


@router.put("/me", response_model=EmployeeResponse)
async def update_me(
    payload: EmployeeUpdateMeRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    return await update_me_controller(current_user["id"], payload.model_dump(), db)


@router.get("", response_model=list[EmployeeResponse])
async def list_employees(
    _: dict = Depends(require_roles("manager", "admin")),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    return await list_employees_controller(db)
