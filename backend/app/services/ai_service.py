import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.models import Incident, Notification, Report, User


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class MockStore:
    def __init__(self) -> None:
        self.users: Dict[str, User] = {}
        self.reports: Dict[str, Report] = {}
        self.incidents: Dict[str, Incident] = {}
        self.notifications: Dict[str, Notification] = {}
        self._seed()

    def _seed(self) -> None:
        # Seed default users
        self.users["student-1"] = User(
            id="student-1",
            name="Aisha Student",
            email="student@civicguard.ai",
            password_hash="$2b$12$SeveralDummyHashForDemo1234567890",
            role="student",
            created_at=utc_now(),
        )
        self.users["worker-1"] = User(
            id="worker-1",
            name="Nikhil Worker",
            email="worker@civicguard.ai",
            password_hash="$2b$12$SeveralDummyHashForDemo1234567890",
            role="worker",
            created_at=utc_now(),
        )
        self.users["admin-1"] = User(
            id="admin-1",
            name="Priya Admin",
            email="admin@civicguard.ai",
            password_hash="$2b$12$SeveralDummyHashForDemo1234567890",
            role="admin",
            created_at=utc_now(),
        )

        report_1 = Report(
            id="report-1",
            reporter_id="student-1",
            reporter_name="Aisha Student",
            category="POTHOLE",
            description="Large pothole near main gate causing risk to students.",
            latitude=12.9716,
            longitude=77.5946,
            location="Main Gate, Campus",
            status="OPEN",
            issue_type="POTHOLE",
            ai_summary="Large pothole near main gate with high pedestrian traffic.",
            created_at=utc_now(),
            incident_id="INC-001",
            is_duplicate=False,
        )
        report_2 = Report(
            id="report-2",
            reporter_id="student-1",
            reporter_name="Aisha Student",
            category="ROAD_DAMAGE",
            description="Road damaged near entrance and there is a huge hole.",
            latitude=12.9718,
            longitude=77.5949,
            location="Main Entrance",
            status="OPEN",
            issue_type="POTHOLE",
            ai_summary="Similar to a pothole near campus entrance.",
            created_at=utc_now(),
            incident_id="INC-001",
            is_duplicate=True,
        )
        report_3 = Report(
            id="report-3",
            reporter_id="student-1",
            reporter_name="Aisha Student",
            category="STREETLIGHT",
            description="Streetlight near the library is flickering and unsafe at night.",
            latitude=12.9722,
            longitude=77.5958,
            location="Library Road",
            status="OPEN",
            issue_type="STREETLIGHT",
            ai_summary="Flickering streetlight near pedestrian corridor.",
            created_at=utc_now(),
            incident_id=None,
            is_duplicate=False,
        )

        self.reports[report_1.id] = report_1
        self.reports[report_2.id] = report_2
        self.reports[report_3.id] = report_3

        self.incidents["INC-001"] = Incident(
            id="INC-001",
            title="Pothole near Main Gate",
            category="POTHOLE",
            description="Large pothole near the main gate with repeated reports.",
            priority="P1",
            department="Maintenance",
            status="ACTIVE",
            latitude=12.9717,
            longitude=77.5948,
            location="Main Gate, Campus",
            supporting_report_ids=[report_1.id, report_2.id],
            assigned_worker_id="worker-1",
            assigned_worker_name="Nikhil Worker",
            ai_summary="Multiple reports indicate a significant road hazard near the main entrance.",
            created_at=utc_now(),
            updated_at=utc_now(),
        )

        self.notifications["notif-1"] = Notification(
            id="notif-1",
            user_id="admin-1",
            message="New incident INC-001 created from clustered student reports.",
            type="incident",
            created_at=utc_now(),
        )

        self.notifications["notif-2"] = Notification(
            id="notif-2",
            user_id="student-1",
            message="Your report was merged into incident INC-001.",
            type="update",
            created_at=utc_now(),
        )

    def get_user_by_email(self, email: str) -> Optional[User]:
        for user in self.users.values():
            if user.email.lower() == email.lower():
                return user
        return None

    def create_user(self, user: User) -> User:
        self.users[user.id] = user
        return user

    def create_report(self, report: Report) -> Report:
        self.reports[report.id] = report
        return report

    def create_incident(self, incident: Incident) -> Incident:
        self.incidents[incident.id] = incident
        return incident

    def create_notification(self, notification: Notification) -> Notification:
        self.notifications[notification.id] = notification
        return notification

    def list_reports(self) -> List[Report]:
        return list(self.reports.values())

    def list_incidents(self) -> List[Incident]:
        return list(self.incidents.values())

    def list_notifications(self, user_id: Optional[str] = None) -> List[Notification]:
        if user_id is None:
            return list(self.notifications.values())
        return [n for n in self.notifications.values() if n.user_id == user_id]

    def get_incident(self, incident_id: str) -> Optional[Incident]:
        return self.incidents.get(incident_id)

    def save_incident(self, incident: Incident) -> Incident:
        self.incidents[incident.id] = incident
        return incident
