from datetime import date

from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.controllers.record_controller import (
    all_records_controller,
    approve_record_controller,
    create_record_controller,
    my_records_controller,
    reject_record_controller,
)
from app.core.dependencies import get_current_user, get_db, require_roles
from app.schemas.record_schema import RecordCreateRequest, RecordResponse


router = APIRouter()


@router.post("", response_model=RecordResponse)
async def create_record(
    payload: RecordCreateRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    return await create_record_controller(current_user["id"], payload.model_dump(), db)


@router.get("/my", response_model=list[RecordResponse])
async def my_records(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    return await my_records_controller(current_user["id"], db)


@router.get("", response_model=list[RecordResponse])
async def all_records(
    employee_id: str | None = Query(default=None),
    type: str | None = Query(default=None),
    status: str | None = Query(default=None),
    from_date: date | None = Query(default=None),
    to_date: date | None = Query(default=None),
    _: dict = Depends(require_roles("manager", "admin")),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    filters = {
        "employee_id": employee_id,
        "type": type,
        "status": status,
        "from_date": from_date,
        "to_date": to_date,
    }
    return await all_records_controller(filters, db)


@router.put("/{id}/approve", response_model=RecordResponse)
async def approve_record(
    id: str,
    _: dict = Depends(require_roles("manager", "admin")),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    return await approve_record_controller(id, db)


@router.put("/{id}/reject", response_model=RecordResponse)
async def reject_record(
    id: str,
    _: dict = Depends(require_roles("manager", "admin")),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    return await reject_record_controller(id, db)
