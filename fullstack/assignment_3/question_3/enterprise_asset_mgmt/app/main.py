from fastapi import FastAPI
from app.database.session import engine
from app.database.base import Base
from app.routers import auth_router, superadmin_router, itadmin_router, manager_router, employee_router

app = FastAPI(title="Enterprise Asset Management")


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "Enterprise Asset Management API is running"}


app.include_router(auth_router)
app.include_router(superadmin_router)
app.include_router(itadmin_router)
app.include_router(manager_router)
app.include_router(employee_router)
