from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.models import Incident, Notification
from app.services.auth_service import decode_token
from app.services.mock_store import MockStore

router = APIRouter()
store = MockStore()


class DashboardStats(BaseModel):
    total_reports: int
    total_incidents: int
    critical_issues: int
    high_priority_issues: int
    active_issues: int
    resolved_issues: int
    avg_resolution_time_hours: float


class AssignmentRequest(BaseModel):
    incident_id: str
    worker_id: str


def verify_admin(authorization: Optional[str]) -> str:
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    parts = authorization.split()
    if len(parts) != 2:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        payload = decode_token(parts[1])
        if payload.get("role") != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        return payload.get("sub")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard(authorization: Optional[str] = None):
    verify_admin(authorization)
    incidents = list(store.incidents.values())
    resolved = [i for i in incidents if i.status == "RESOLVED"]
    total_time = 0.0
    for i in resolved:
        if i.resolved_at and i.created_at:
            diff = datetime.fromisoformat(i.resolved_at) - datetime.fromisoformat(i.created_at)
            total_time += diff.total_seconds()
    avg = (total_time / len(resolved) / 3600) if resolved else 0.0
    return DashboardStats(
        total_reports=len(store.reports),
        total_incidents=len(store.incidents),
        critical_issues=len([i for i in incidents if i.priority == "P1"]),
        high_priority_issues=len([i for i in incidents if i.priority == "P2"]),
        active_issues=len([i for i in incidents if i.status in ["ACTIVE", "ASSIGNED", "IN_PROGRESS"]]),
        resolved_issues=len(resolved),
        avg_resolution_time_hours=avg,
    )


@router.post("/assign-worker")
def assign_worker(request: AssignmentRequest, authorization: Optional[str] = None):
    verify_admin(authorization)
    incident = store.incidents.get(request.incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    worker = store.users.get(request.worker_id)
    if not worker or worker.role != "worker":
        raise HTTPException(status_code=404, detail="Worker not found")
    incident.assigned_worker_id = worker.id
    incident.assigned_worker_name = worker.name
    incident.status = "ASSIGNED"
    incident.updated_at = datetime.now(timezone.utc).isoformat()
    store.save_incident(incident)
    store.create_notification(
        Notification(
            id=f"notif-{uuid4().hex[:8]}",
            user_id=worker.id,
            message=f"New incident assigned: {incident.title}",
            type="assignment",
            read=False,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
    )
    return {"status": "assigned", "incident_id": incident.id}


@router.get("/all-reports")
def get_all_reports(authorization: Optional[str] = None):
    verify_admin(authorization)
    return list(store.reports.values())


@router.get("/all-incidents")
def get_all_incidents(authorization: Optional[str] = None):
    verify_admin(authorization)
    return list(store.incidents.values())
