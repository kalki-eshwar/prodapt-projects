import os

files = {
    ".env": "DATABASE_URL=sqlite:///./test.db\nSECRET_KEY=yoursecretkey\nALGORITHM=HS256\nACCESS_TOKEN_EXPIRE_MINUTES=30\nSUPERADMIN_EMAIL=admin@example.com\nSUPERADMIN_PASSWORD=admin",
    "requirements.txt": "fastapi\nuvicorn\nsqlalchemy\npydantic\npasslib[bcrypt]\npython-jose\npytest\nhttpx\npython-dotenv\npydantic-settings\n",
    "app/__init__.py": "",
    "app/main.py": "from fastapi import FastAPI\n\napp = FastAPI(title='EAMS')\n\n@app.get('/')\ndef root(): return {'message': 'EAMS API'}",
    "app/core/__init__.py": "",
    "app/core/config.py": "from pydantic_settings import BaseSettings\nclass Settings(BaseSettings):\n    DATABASE_URL: str = 'sqlite:///./test.db'\n    SECRET_KEY: str = 'secret'\n    ALGORITHM: str = 'HS256'\n    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30\n    class Config:\n        env_file = '.env'\nsettings = Settings()",
    "app/core/security.py": "from passlib.context import CryptContext\npwd_context = CryptContext(schemes=['bcrypt'])\ndef verify_password(plain_password, hashed_password): return pwd_context.verify(plain_password, hashed_password)\ndef get_password_hash(password): return pwd_context.hash(password)",
    "app/core/pagination.py": "# Pagination",
    "app/database/__init__.py": "",
    "app/database/base.py": "from sqlalchemy.ext.declarative import declarative_base\nBase = declarative_base()",
    "app/database/session.py": "from sqlalchemy import create_engine\nfrom sqlalchemy.orm import sessionmaker\nfrom app.core.config import settings\nengine = create_engine(settings.DATABASE_URL, connect_args={'check_same_thread': False})\nSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)\ndef get_db():\n    db = SessionLocal()\n    try: yield db\n    finally: db.close()",
    "app/models/__init__.py": "from .user import User\nfrom .department import Department\nfrom .asset import Asset\nfrom .asset_assignment import AssetAssignment\nfrom .asset_request import AssetRequest",
    "app/models/user.py": "from sqlalchemy import Column, Integer, String, ForeignKey\nfrom sqlalchemy.orm import relationship\nfrom app.database.base import Base\nclass User(Base):\n    __tablename__ = 'users'\n    id = Column(Integer, primary_key=True, index=True)\n    name = Column(String)\n    email = Column(String, unique=True, index=True)\n    password = Column(String)\n    role = Column(String)\n    department_id = Column(Integer, ForeignKey('departments.id'))\n    department = relationship('Department', foreign_keys=[department_id])",
    "app/models/department.py": "from sqlalchemy import Column, Integer, String, ForeignKey\nfrom sqlalchemy.orm import relationship\nfrom app.database.base import Base\nclass Department(Base):\n    __tablename__ = 'departments'\n    id = Column(Integer, primary_key=True, index=True)\n    name = Column(String, unique=True)\n    manager_id = Column(Integer, ForeignKey('users.id'))",
    "app/models/asset.py": "from sqlalchemy import Column, Integer, String, ForeignKey, DateTime\nfrom app.database.base import Base\nclass Asset(Base):\n    __tablename__ = 'assets'\n    id = Column(Integer, primary_key=True, index=True)\n    asset_tag = Column(String, unique=True, index=True)\n    asset_type = Column(String)\n    brand = Column(String)\n    model = Column(String)\n    status = Column(String, default='AVAILABLE')\n    department_id = Column(Integer, ForeignKey('departments.id'))",
    "app/models/asset_assignment.py": "from sqlalchemy import Column, Integer, String, ForeignKey, DateTime\nfrom app.database.base import Base\nclass AssetAssignment(Base):\n    __tablename__ = 'asset_assignments'\n    id = Column(Integer, primary_key=True, index=True)\n    asset_id = Column(Integer, ForeignKey('assets.id'))\n    user_id = Column(Integer, ForeignKey('users.id'))\n    assigned_date = Column(DateTime)\n    returned_date = Column(DateTime, nullable=True)\n    condition_on_return = Column(String, nullable=True)",
    "app/models/asset_request.py": "from sqlalchemy import Column, Integer, String, ForeignKey\nfrom app.database.base import Base\nclass AssetRequest(Base):\n    __tablename__ = 'asset_requests'\n    id = Column(Integer, primary_key=True, index=True)\n    employee_id = Column(Integer, ForeignKey('users.id'))\n    asset_type = Column(String)\n    reason = Column(String)\n    status = Column(String, default='PENDING')\n    approved_by = Column(Integer, ForeignKey('users.id'), nullable=True)",
    "app/schemas/__init__.py": "",
    "app/schemas/user_schema.py": "from pydantic import BaseModel\nfrom typing import Optional\nclass UserCreate(BaseModel):\n    name: str\n    email: str\n    password: str\n    role: str\n    department_id: Optional[int] = None",
    "app/schemas/department_schema.py": "",
    "app/schemas/asset_schema.py": "",
    "app/schemas/assignment_schema.py": "",
    "app/schemas/request_schema.py": "",
    "app/repositories/__init__.py": "",
    "app/repositories/user_repo.py": "",
    "app/repositories/department_repo.py": "",
    "app/repositories/asset_repo.py": "",
    "app/repositories/assignment_repo.py": "",
    "app/repositories/request_repo.py": "",
    "app/services/__init__.py": "",
    "app/services/auth_service.py": "",
    "app/services/asset_service.py": "",
    "app/services/assignment_service.py": "",
    "app/services/request_service.py": "",
    "app/controllers/__init__.py": "",
    "app/controllers/auth_controller.py": "",
    "app/controllers/superadmin_controller.py": "",
    "app/controllers/itadmin_controller.py": "",
    "app/controllers/manager_controller.py": "",
    "app/controllers/employee_controller.py": "",
    "app/dependencies/__init__.py": "",
    "app/dependencies/rbac.py": "from fastapi import HTTPException\ndef require_roles(*roles):\n    def wrapper(current_user: dict):\n        if current_user.get('role') not in roles:\n            raise HTTPException(status_code=403)\n        return current_user\n    return wrapper",
    "app/middleware/__init__.py": "",
    "app/middleware/logging.py": "",
    "app/middleware/exception_handler.py": "",
    "app/routers/__init__.py": "",
    "app/routers/auth_router.py": "",
    "app/routers/superadmin_router.py": "",
    "app/routers/itadmin_router.py": "",
    "app/routers/manager_router.py": "",
    "app/routers/employee_router.py": "",
    "tests/__init__.py": "",
    "tests/test_auth.py": "def test_auth_dummy():\n    assert True",
    "tests/test_asset.py": "def test_asset_dummy():\n    assert True",
    "tests/test_assignment.py": "def test_assignment_dummy():\n    assert True"
}

for path, content in files.items():
    if "/" in path:
        os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

with open("app/main.py", "w") as f:
    f.write("from fastapi import FastAPI\nfrom app.database.base import Base\nfrom app.database.session import engine\nimport app.models # trigger metadata\nBase.metadata.create_all(bind=engine)\n\napp = FastAPI(title='EAMS')\n\n@app.get('/')\ndef root(): return {'message': 'EAMS API'}")
