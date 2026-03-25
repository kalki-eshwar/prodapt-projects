def _auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def test_employee_creation_and_profile_flow(client):
    admin_register = client.post(
        "/auth/register",
        json={"email": "admin@example.com", "password": "admin123", "role": "admin"},
    )
    assert admin_register.status_code == 200
    admin_token = admin_register.json()["access_token"]

    employee_create = client.post(
        "/admin/employees",
        json={
            "email": "employee1@example.com",
            "password": "employee123",
            "role": "employee",
            "name": "Emp One",
            "department": "Engineering",
            "manager_id": None,
        },
        headers=_auth_header(admin_token),
    )
    assert employee_create.status_code == 200

    employee_login = client.post(
        "/auth/login",
        json={"email": "employee1@example.com", "password": "employee123"},
    )
    assert employee_login.status_code == 200
    employee_token = employee_login.json()["access_token"]

    me = client.get("/employees/me", headers=_auth_header(employee_token))
    assert me.status_code == 200
    assert me.json()["department"] == "Engineering"


def test_leave_approval_flow(client):
    admin = client.post(
        "/auth/register",
        json={"email": "admin2@example.com", "password": "admin123", "role": "admin"},
    )
    assert admin.status_code == 200
    admin_token = admin.json()["access_token"]

    manager_create = client.post(
        "/admin/employees",
        json={
            "email": "manager@example.com",
            "password": "manager123",
            "role": "manager",
            "name": "Mgr One",
            "department": "Engineering",
            "manager_id": None,
        },
        headers=_auth_header(admin_token),
    )
    assert manager_create.status_code == 200
    manager_profile_id = manager_create.json()["employee"]["id"]

    employee_create = client.post(
        "/admin/employees",
        json={
            "email": "employee2@example.com",
            "password": "employee123",
            "role": "employee",
            "name": "Emp Two",
            "department": "Engineering",
            "manager_id": manager_profile_id,
        },
        headers=_auth_header(admin_token),
    )
    assert employee_create.status_code == 200

    employee_login = client.post(
        "/auth/login",
        json={"email": "employee2@example.com", "password": "employee123"},
    )
    employee_token = employee_login.json()["access_token"]

    leave_request = client.post(
        "/records",
        json={"type": "leave", "from_date": "2026-03-01", "to_date": "2026-03-03"},
        headers=_auth_header(employee_token),
    )
    assert leave_request.status_code == 200
    leave_id = leave_request.json()["id"]

    manager_login = client.post(
        "/auth/login",
        json={"email": "manager@example.com", "password": "manager123"},
    )
    manager_token = manager_login.json()["access_token"]

    approve = client.put(f"/records/{leave_id}/approve", headers=_auth_header(manager_token))
    assert approve.status_code == 200
    assert approve.json()["status"] == "approved"


def test_attendance_tracking(client):
    register = client.post(
        "/auth/register",
        json={"email": "employee3@example.com", "password": "employee123", "role": "employee"},
    )
    token = register.json()["access_token"]

    # Without a profile, attendance should fail.
    missing_profile = client.post(
        "/records",
        json={"type": "attendance", "date": "2026-03-04"},
        headers=_auth_header(token),
    )
    assert missing_profile.status_code == 404
