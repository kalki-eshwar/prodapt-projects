from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from jose import JWTError
from sqlalchemy.exc import SQLAlchemyError
from app.routers import auth_router, admin_router, manager_router, employee_router
from app.middleware.logging import log_requests
from app.middleware.exception_handler import (
    validation_exception_handler,
    sqlalchemy_exception_handler,
    jwt_exception_handler
)
from app.database.session import engine
from app.database.base import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Enterprise Leave Management System")

# Middleware
app.middleware("http")(log_requests)

# Exception Handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(JWTError, jwt_exception_handler)

# Routers
app.include_router(auth_router.router)
app.include_router(admin_router.router)
app.include_router(manager_router.router)
app.include_router(employee_router.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Enterprise Leave Management System API"}
