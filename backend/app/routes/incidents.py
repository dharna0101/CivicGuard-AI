from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.auth_service import decode_token
from app.services.mock_store import MockStore

router = APIRouter()
store = MockStore()


class NotificationResponse(BaseModel):
    id: str
    user_id: str
    message: str
    type: str
    read: bool
    created_at: str


@router.get("/", response_model=List[NotificationResponse])
def get_notifications(authorization: Optional[str] = None):
    if not authorization:
        raise HTTPException(status_code=401)
    parts = authorization.split()
    if len(parts) != 2:
        raise HTTPException(status_code=401)
    try:
        payload = decode_token(parts[1])
        user_id = payload.get("sub")
        notifications = store.list_notifications(user_id)
        return [
            NotificationResponse(
                id=n.id,
                user_id=n.user_id,
                message=n.message,
                type=n.type,
                read=n.read,
                created_at=n.created_at,
            )
            for n in notifications
        ]
    except Exception:
        raise HTTPException(status_code=401)
