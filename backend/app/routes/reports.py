from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.mock_store import MockStore

router = APIRouter()
store = MockStore()


class IncidentResponse(BaseModel):
    id: str
    title: str
    category: str
    description: str
    priority: str
    department: str
    status: str
    latitude: float
    longitude: float
    location: str
    supporting_report_ids: List[str]
    assigned_worker_id: Optional[str]
    assigned_worker_name: Optional[str]
    resolution_notes: Optional[str]
    ai_summary: Optional[str]
    created_at: str
    updated_at: str
    resolved_at: Optional[str]
    is_reopened: bool


@router.get("/", response_model=List[IncidentResponse])
def list_incidents():
    incidents = list(store.incidents.values())
    return [
        IncidentResponse(
            id=i.id,
            title=i.title,
            category=i.category,
            description=i.description,
            priority=i.priority,
            department=i.department,
            status=i.status,
            latitude=i.latitude,
            longitude=i.longitude,
            location=i.location,
            supporting_report_ids=i.supporting_report_ids,
            assigned_worker_id=i.assigned_worker_id,
            assigned_worker_name=i.assigned_worker_name,
            resolution_notes=i.resolution_notes,
            ai_summary=i.ai_summary,
            created_at=i.created_at,
            updated_at=i.updated_at,
            resolved_at=i.resolved_at,
            is_reopened=i.is_reopened,
        )
        for i in incidents
    ]


@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(incident_id: str):
    incident = store.incidents.get(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return IncidentResponse(
        id=incident.id,
        title=incident.title,
        category=incident.category,
        description=incident.description,
        priority=incident.priority,
        department=incident.department,
        status=incident.status,
        latitude=incident.latitude,
        longitude=incident.longitude,
        location=incident.location,
        supporting_report_ids=incident.supporting_report_ids,
        assigned_worker_id=incident.assigned_worker_id,
        assigned_worker_name=incident.assigned_worker_name,
        resolution_notes=incident.resolution_notes,
        ai_summary=incident.ai_summary,
        created_at=incident.created_at,
        updated_at=incident.updated_at,
        resolved_at=incident.resolved_at,
        is_reopened=incident.is_reopened,
    )
