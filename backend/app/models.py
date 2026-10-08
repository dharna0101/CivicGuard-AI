from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class User:
    id: str
    name: str
    email: str
    password_hash: str
    role: str
    phone: Optional[str] = None
    created_at: str = ""


@dataclass
class Report:
    id: str
    reporter_id: str
    reporter_name: str
    category: str
    description: str
    latitude: float
    longitude: float
    location: str
    image_url: Optional[str] = None
    status: str = "OPEN"
    issue_type: Optional[str] = None
    ai_summary: Optional[str] = None
    created_at: str = ""
    incident_id: Optional[str] = None
    is_duplicate: bool = False


@dataclass
class Incident:
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
    supporting_report_ids: List[str] = field(default_factory=list)
    assigned_worker_id: Optional[str] = None
    assigned_worker_name: Optional[str] = None
    resolution_notes: Optional[str] = None
    ai_summary: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""
    resolved_at: Optional[str] = None
    is_reopened: bool = False


@dataclass
class Notification:
    id: str
    user_id: str
    message: str
    type: str
    read: bool = False
    created_at: str = ""
