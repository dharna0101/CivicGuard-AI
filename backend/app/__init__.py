from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from app.models import Notification
from app.services.auth_service import decode_token
from app.services.mock_store import MockStore
from uuid import uuid4

router = APIRouter()
store = MockStore()


def verify_worker(authorization: Optional[str]) -> str:
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    parts = authorization.split()
    if len(parts) != 2:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        payload = decode_token(parts[1])
        if payload.get("role") != "worker":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        return payload.get("sub")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/assigned-incidents")
def get_assigned_incidents(authorization: Optional[str] = None):
    worker_id = verify_worker(authorization)
    return [i for i in store.incidents.values() if i.assigned_worker_id == worker_id]


@router.post("/start-work/{incident_id}")
def start_work(incident_id: str, authorization: Optional[str] = None):
    verify_worker(authorization)
    incident = store.incidents.get(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    incident.status = "IN_PROGRESS"
    incident.updated_at = datetime.now(timezone.utc).isoformat()
    store.save_incident(incident)
    return {"status": "work started", "incident_id": incident.id}


@router.post("/submit-resolution/{incident_id}")
async def submit_resolution(
    incident_id: str,
    resolution_notes: str = Form(...),
    file: Optional[UploadFile] = File(None),
    authorization: Optional[str] = None,
):
    verify_worker(authorization)
    incident = store.incidents.get(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    image_url = None
    if file:
        from app.config import UPLOAD_DIR

        file_path = UPLOAD_DIR / f"{incident_id}-{file.filename}"
        file_path.write_bytes(await file.read())
        image_url = f"/uploads/{file_path.name}"

    incident.resolution_notes = resolution_notes
    incident.status = "COMPLETED"
    incident.updated_at = datetime.now(timezone.utc).isoformat()
    store.save_incident(incident)

    admin_user = next((u for u in store.users.values() if u.role == "admin"), None)
    if admin_user:
        store.create_notification(
            Notification(
                id=f"notif-{uuid4().hex[:8]}",
                user_id=admin_user.id,
                message=f"Resolution submitted for incident {incident.id}: {incident.title}",
                type="resolution_pending",
                read=False,
                created_at=datetime.now(timezone.utc).isoformat(),
            )
        )

    return {"status": "resolution submitted", "incident_id": incident.id, "image_url": image_url}

