import uuid

import httpx


BASE_URL = "http://127.0.0.1:8000"


def run() -> int:
    results: list[tuple[str, bool, str]] = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        results.append((name, condition, detail))

    def request(method: str, path: str, token: str | None = None, json: dict | None = None, params: dict | None = None):
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return httpx.request(method, f"{BASE_URL}{path}", headers=headers, json=json, params=params, timeout=20)

    seed = uuid.uuid4().hex[:8]
    admin_email = f"admin_{seed}@example.com"
    manager_email = f"mgr_{seed}@example.com"
    emp1_email = f"emp1_{seed}@example.com"
    emp2_email = f"emp2_{seed}@example.com"

    r = request("GET", "/health")
    check("health", r.status_code == 200 and r.json().get("status") == "ok", r.text)

    r = request("POST", "/auth/register", json={"email": admin_email, "password": "admin123", "role": "admin"})
    check("auth.register.admin", r.status_code == 200, r.text)
    admin_token = r.json().get("access_token") if r.status_code == 200 else None

    r = request("POST", "/auth/login", json={"email": admin_email, "password": "admin123"})
    check("auth.login.admin", r.status_code == 200, r.text)

    r = request(
        "POST",
        "/admin/employees",
        token=admin_token,
        json={
            "email": manager_email,
            "password": "manager123",
            "role": "manager",
            "name": "Mgr Test",
            "department": "Engineering",
            "manager_id": None,
        },
    )
    check("admin.create.manager", r.status_code == 200, r.text)
    manager_employee_id = r.json().get("employee", {}).get("id") if r.status_code == 200 else None

    r = request(
        "POST",
        "/admin/employees",
        token=admin_token,
        json={
            "email": emp1_email,
            "password": "emp123",
            "role": "employee",
            "name": "Emp One",
            "department": "Engineering",
            "manager_id": manager_employee_id,
        },
    )
    check("admin.create.employee1", r.status_code == 200, r.text)
    emp1_employee_id = r.json().get("employee", {}).get("id") if r.status_code == 200 else None

    r = request(
        "POST",
        "/admin/employees",
        token=admin_token,
        json={
            "email": emp2_email,
            "password": "emp123",
            "role": "employee",
            "name": "Emp Two",
            "department": "QA",
            "manager_id": manager_employee_id,
        },
    )
    check("admin.create.employee2", r.status_code == 200, r.text)
    emp2_employee_id = r.json().get("employee", {}).get("id") if r.status_code == 200 else None

    r = request("POST", "/auth/login", json={"email": emp1_email, "password": "emp123"})
    check("auth.login.employee", r.status_code == 200, r.text)
    emp1_token = r.json().get("access_token") if r.status_code == 200 else None

    r = request("GET", "/employees/me", token=emp1_token)
    check("employees.me.get", r.status_code == 200 and r.json().get("name") == "Emp One", r.text)

    r = request("PUT", "/employees/me", token=emp1_token, json={"name": "Emp One Updated", "department": "Platform"})
    check("employees.me.put", r.status_code == 200 and r.json().get("department") == "Platform", r.text)

    r = request("POST", "/auth/login", json={"email": manager_email, "password": "manager123"})
    check("auth.login.manager", r.status_code == 200, r.text)
    manager_token = r.json().get("access_token") if r.status_code == 200 else None

    r = request("GET", "/employees", token=manager_token)
    check("employees.list.manager", r.status_code == 200 and len(r.json()) >= 3, r.text)

    r = request("GET", "/employees", token=emp1_token)
    check("employees.list.employee.forbidden", r.status_code == 403, str(r.status_code))

    r = request("POST", "/records", token=emp1_token, json={"type": "attendance", "date": "2026-03-05"})
    check("records.create.attendance", r.status_code == 200 and r.json().get("status") == "approved", r.text)
    attendance_id = r.json().get("id") if r.status_code == 200 else None

    r = request("POST", "/records", token=emp1_token, json={"type": "leave", "from_date": "2026-03-06", "to_date": "2026-03-07"})
    check("records.create.leave", r.status_code == 200 and r.json().get("status") == "pending", r.text)
    leave_id = r.json().get("id") if r.status_code == 200 else None

    r = request("GET", "/records/my", token=emp1_token)
    check("records.my", r.status_code == 200 and len(r.json()) >= 2, r.text)

    r = request("GET", "/records", token=manager_token)
    check("records.all.manager", r.status_code == 200 and len(r.json()) >= 2, r.text)

    r = request(
        "GET",
        "/records",
        token=manager_token,
        params={"employee_id": emp1_employee_id, "type": "leave", "status": "pending"},
    )
    check("records.all.query.employee_type_status", r.status_code == 200 and any(x.get("id") == leave_id for x in r.json()), r.text)

    r = request("GET", "/records", token=manager_token, params={"from_date": "2026-03-01", "to_date": "2026-03-10"})
    check("records.all.query.date_range", r.status_code == 200 and len(r.json()) >= 2, r.text)

    r = request("PUT", f"/records/{leave_id}/approve", token=manager_token)
    check("records.approve.leave", r.status_code == 200 and r.json().get("status") == "approved", r.text)

    r = request("PUT", f"/records/{attendance_id}/reject", token=manager_token)
    check("records.reject.attendance.invalid", r.status_code == 422, str(r.status_code))

    r = request("PUT", f"/admin/employees/{emp2_employee_id}", token=admin_token, json={"department": "Support"})
    check("admin.update.employee", r.status_code == 200 and r.json().get("department") == "Support", r.text)

    r = request("GET", "/admin/reports", token=admin_token)
    report = r.json() if r.status_code == 200 else {}
    check("admin.reports", r.status_code == 200 and "total_employees" in report and "total_records" in report, r.text)

    r = request("DELETE", f"/admin/employees/{emp2_employee_id}", token=admin_token)
    check("admin.delete.employee", r.status_code == 200 and r.json().get("deleted") is True, r.text)

    failed = [item for item in results if not item[1]]
    for name, ok, detail in results:
        print(("PASS" if ok else "FAIL"), name, "" if ok else detail[:220])

    print("TOTAL", len(results), "FAILED", len(failed))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(run())
