from fastapi import APIRouter

from app.api.routes import admin, auth, employees, records


api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(employees.router, prefix="/employees", tags=["employees"])
api_router.include_router(records.router, prefix="/records", tags=["records"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
