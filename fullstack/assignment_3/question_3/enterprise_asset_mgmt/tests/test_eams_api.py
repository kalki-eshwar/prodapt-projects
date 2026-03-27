import os
from fastapi.testclient import TestClient
from app.main import app

from app.database.session import engine
from app.database.base import Base

client = TestClient(app)


def setup_module(module):
    # Ensure clean DB for tests
    db_file = "enterprise_asset.db"
    if os.path.exists(db_file):
        os.remove(db_file)
    Base.metadata.create_all(bind=engine)


def test_full_workflow():
    # Register users
    superadmin_payload = {"name": "Super Admin", "email": "admin@example.com", "password": "pass", "role": "SUPERADMIN"}
    emp_payload = {"name": "Employee", "email": "emp@example.com", "password": "pass", "role": "EMPLOYEE"}

    resp_admin = client.post("/auth/register", json=superadmin_payload)
    assert resp_admin.status_code == 200
    superadmin_id = resp_admin.json()["id"]

    resp_emp = client.post("/auth/register", json=emp_payload)
    assert resp_emp.status_code == 200
    employee_id = resp_emp.json()["id"]

    # Create department
    dept_resp = client.post("/superadmin/departments", json={"name": "IT", "manager_id": None}, headers={"X-User-Id": str(superadmin_id)})
    assert dept_resp.status_code == 200
    department_id = dept_resp.json()["id"]

    # Create asset
    asset_resp = client.post(
        "/itadmin/assets",
        json={"asset_tag": "TAG001", "asset_type": "Laptop", "brand": "Dell", "model": "XPS", "status": "AVAILABLE", "department_id": department_id},
        headers={"X-User-Id": str(superadmin_id)},
    )
    assert asset_resp.status_code == 200
    asset_id = asset_resp.json()["id"]

    # Assign asset
    from datetime import date
    assign_resp = client.post(
        "/itadmin/assignments",
        json={"asset_id": asset_id, "user_id": employee_id, "assigned_date": str(date.today())},
        headers={"X-User-Id": str(superadmin_id)},
    )
    assert assign_resp.status_code == 200
    assignment_id = assign_resp.json()["id"]

    # Employee views own assets
    emp_assets_resp = client.get("/employee/my-assets", headers={"X-User-Id": str(employee_id)})
    assert emp_assets_resp.status_code == 200
    assert len(emp_assets_resp.json()) == 1

    # Return assignment
    return_resp = client.patch(
        f"/itadmin/assignments/{assignment_id}",
        json={"returned_date": str(date.today()), "condition_on_return": "Good"},
        headers={"X-User-Id": str(superadmin_id)},
    )
    assert return_resp.status_code == 200

    # Create request as employee
    req_resp = client.post(
        "/employee/requests",
        json={"employee_id": employee_id, "asset_type": "Laptop", "reason": "Need for development"},
        headers={"X-User-Id": str(employee_id)},
    )
    assert req_resp.status_code == 200
    request_id = req_resp.json()["id"]

    # Approve request as itadmin
    approve_resp = client.post(
        f"/itadmin/requests/{request_id}/approve",
        json={"status": "APPROVED", "approved_by": superadmin_id},
        headers={"X-User-Id": str(superadmin_id)},
    )
    assert approve_resp.status_code == 200
    assert approve_resp.json()["status"] == "APPROVED"


def teardown_module(module):
    Base.metadata.drop_all(bind=engine)
