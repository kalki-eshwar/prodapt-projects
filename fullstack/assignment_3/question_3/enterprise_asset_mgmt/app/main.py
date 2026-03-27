from fastapi import FastAPI
from app.database.base import Base
from app.database.session import engine
import app.models
from app.routers import auth_router, superadmin_router, itadmin_router, manager_router, employee_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title='EAMS')

app.include_router(auth_router.router)
app.include_router(superadmin_router.router)
app.include_router(itadmin_router.router)
app.include_router(manager_router.router)
app.include_router(employee_router.router)

@app.get('/')
def root(): return {'message': 'EAMS API Root'}