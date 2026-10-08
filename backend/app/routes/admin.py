from datetime import datetime, timezone
from typing import List, Optional
from uuid import uuid4

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from app.config import UPLOAD_DIR
from app.models import Incident, Notification, Report
from app.services.ai_service import analyze_report, calculate_priority, calculate_similarity
from app.services.auth_service import decode_token
from app.services.mock_store import MockStore

router = APIRouter()
store = MockStore()


class ReportResponse(BaseModel):
    id: str
    reporter_id: str
    reporter_name: str
    category: str
    description: str
    latitude: float
    longitude: float
    location: str
    image_url: Optional[str]
    status: str
    issue_type: Optional[str]
    ai_summary: Optional[str]
    created_at: str
    incident_id: Optional[str]
    is_duplicate: bool


def get_auth_header(authorization: Optional[str] = None) -> dict:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    try:
        return decode_token(parts[1])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/submit", response_model=ReportResponse)
async def submit_report(
    category: str = Form(...),
    description: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    location: str = Form(...),
    file: Optional[UploadFile] = File(None),
    authorization: Optional[str] = None,
):
    payload = get_auth_header(authorization)
    user_id = payload.get("sub")
    user = store.users.get(user_id)
    if not user:
        raise HTTPException(status_code=401)

    report_id = f"report-{uuid4().hex[:8]}"
    image_url = None
    if file:
        file_path = UPLOAD_DIR / f"{report_id}-{file.filename}"
        file_path.write_bytes(await file.read())
        image_url = f"/uploads/{file_path.name}"

    ai = analyze_report({"category": category, "description": description})
    report = Report(
        id=report_id,
        reporter_id=user_id,
        reporter_name=user.name,
        category=category,
        description=description,
        latitude=latitude,
        longitude=longitude,
        location=location,
        image_url=image_url,
        status="OPEN",
        issue_type=ai.get("issue_type"),
        ai_summary=ai.get("reason"),
        created_at=datetime.now(timezone.utc).isoformat(),
        incident_id=None,
        is_duplicate=False,
    )
    store.create_report(report)

    best_incident = None
    highest_similarity = 0.0
    for incident in store.incidents.values():
        similarity = calculate_similarity(
            {"category": category, "description": description, "latitude": latitude, "longitude": longitude},
            {"category": incident.category, "description": incident.description, "latitude": incident.latitude, "longitude": incident.longitude},
        )
        if similarity >= 0.68 and similarity > highest_similarity:
            best_incident = incident
            highest_similarity = similarity

    if best_incident:
        best_incident.supporting_report_ids.append(report.id)
        best_incident.updated_at = datetime.now(timezone.utc).isoformat()
        report.incident_id = best_incident.id
        report.is_duplicate = True
        store.save_incident(best_incident)
    else:
        incident_id = f"INC-{str(len(store.incidents) + 1).zfill(3)}"
        priority = calculate_priority({
            "severity": ai.get("severity", "MEDIUM"),
            "supporting_report_count": 1,
            "risk_score": 12 if ai.get("safety_risk") == "HIGH" else 8,
        })
        incident = Incident(
            id=incident_id,
            title=f"{ai.get('issue_type', 'Issue')} at {location}",
            category=category,
            description=description,
            priority=priority.get("priority", "P3"),
            department=ai.get("recommended_department", "Administration"),
            status="ACTIVE",
            latitude=latitude,
            longitude=longitude,
            location=location,
            supporting_report_ids=[report.id],
            ai_summary=ai.get("reason"),
            created_at=datetime.now(timezone.utc).isoformat(),
            updated_at=datetime.now(timezone.utc).isoformat(),
            resolved_at=None,
            is_reopened=False,
        )
        store.create_incident(incident)
        report.incident_id = incident_id

    store.create_report(report)

    admin = next((u for u in store.users.values() if u.role == "admin"), None)
    if admin:
        store.create_notification(
            Notification(
                id=f"notif-{uuid4().hex[:8]}",
                user_id=admin.id,
                message=f"New report received: {description[:80]}",
                type="report",
                read=False,
                created_at=datetime.now(timezone.utc).isoformat(),
            )
        )

    return ReportResponse(
        id=report.id,
        reporter_id=report.reporter_id,
        reporter_name=report.reporter_name,
        category=report.category,
        description=report.description,
        latitude=report.latitude,
        longitude=report.longitude,
        location=report.location,
        image_url=report.image_url,
        status=report.status,
        issue_type=report.issue_type,
        ai_summary=report.ai_summary,
        created_at=report.created_at,
        incident_id=report.incident_id,
        is_duplicate=report.is_duplicate,
    )


@router.get("/my-reports", response_model=List[ReportResponse])
def get_my_reports(authorization: Optional[str] = None):
    payload = get_auth_header(authorization)
    user_id = payload.get("sub")
    reports = [r for r in store.reports.values() if r.reporter_id == user_id]
    return [
        ReportResponse(
            id=r.id,
            reporter_id=r.reporter_id,
            reporter_name=r.reporter_name,
            category=r.category,
            description=r.description,
            latitude=r.latitude,
            longitude=r.longitude,
            location=r.location,
            image_url=r.image_url,
            status=r.status,
            issue_type=r.issue_type,
            ai_summary=r.ai_summary,
            created_at=r.created_at,
            incident_id=r.incident_id,
            is_duplicate=r.is_duplicate,
        )
        for r in reports
    ]


@router.get("/{report_id}", response_model=ReportResponse)
def get_report(report_id: str):
    report = store.reports.get(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return ReportResponse(
        id=report.id,
        reporter_id=report.reporter_id,
        reporter_name=report.reporter_name,
        category=report.category,
        description=report.description,
        latitude=report.latitude,
        longitude=report.longitude,
        location=report.location,
        image_url=report.image_url,
        status=report.status,
        issue_type=report.issue_type,
        ai_summary=report.ai_summary,
        created_at=report.created_at,
        incident_id=report.incident_id,
        is_duplicate=report.is_duplicate,
    )
