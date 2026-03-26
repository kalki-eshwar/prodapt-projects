import pytest
from app.models.user import Role
from datetime import date, timedelta
from app.schemas.leave_schema import LeaveStatus

def test_employee_apply_leave(client, employee_token):
    start_date = (date.today() + timedelta(days=1)).isoformat()
    end_date = (date.today() + timedelta(days=3)).isoformat()
    
    response = client.post("/employee/leave", headers={"Authorization": f"Bearer {employee_token}"}, json={
        "start_date": start_date,
        "end_date": end_date,
        "reason": "Vacation"
    })
    
    assert response.status_code == 200
    assert response.json()["status"] == LeaveStatus.PENDING.value

def test_manager_approve_leave(client, employee_token, manager_token):
    # Apply for leave first
    start_date = (date.today() + timedelta(days=5)).isoformat()
    end_date = (date.today() + timedelta(days=7)).isoformat()
    
    apply_resp = client.post("/employee/leave", headers={"Authorization": f"Bearer {employee_token}"}, json={
        "start_date": start_date,
        "end_date": end_date,
        "reason": "Sick Leave"
    })
    
    leave_id = apply_resp.json()["id"]
    
    # Manager approves
    response = client.put(f"/manager/leave/{leave_id}/status", headers={"Authorization": f"Bearer {manager_token}"}, params={
        "status": LeaveStatus.APPROVED.value
    })
    
    assert response.status_code == 200
    assert response.json()["status"] == LeaveStatus.APPROVED.value

def test_unauthorized_access(client, employee_token):
    # Employee tries to access admin route
    response = client.get("/admin/leaves", headers={"Authorization": f"Bearer {employee_token}"})
    assert response.status_code == 403
