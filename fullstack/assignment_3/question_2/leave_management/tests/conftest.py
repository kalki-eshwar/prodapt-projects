import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.base import Base
from app.database.session import get_db
from app.models.user import Role, User
from app.core.security import create_access_token, get_password_hash
from app.models.department import Department

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]

@pytest.fixture(scope="module")
def setup_test_data(db_session):
    # Setup roles and departments
    dept = Department(name="Engineering")
    db_session.add(dept)
    db_session.commit()
    db_session.refresh(dept)
    
    admin = User(name="Admin", email="admin@test.com", password=get_password_hash("pass"), role=Role.ADMIN.value)
    manager = User(name="Manager", email="manager@test.com", password=get_password_hash("pass"), role=Role.MANAGER.value, department_id=dept.id)
    db_session.add_all([admin, manager])
    db_session.commit()
    db_session.refresh(manager)
    
    dept.manager_id = manager.id
    
    db_session.commit()
    
    employee = User(name="Employee", email="emp@test.com", password=get_password_hash("pass"), role=Role.EMPLOYEE.value, department_id=dept.id)
    db_session.add(employee)
    db_session.commit()

@pytest.fixture(scope="module")
def admin_token(client, setup_test_data):
    return create_access_token(data={"sub": "admin@test.com", "role": Role.ADMIN.value})

@pytest.fixture(scope="module")
def manager_token(client, setup_test_data):
    return create_access_token(data={"sub": "manager@test.com", "role": Role.MANAGER.value})

@pytest.fixture(scope="module")
def employee_token(client, setup_test_data):
    return create_access_token(data={"sub": "emp@test.com", "role": Role.EMPLOYEE.value})
