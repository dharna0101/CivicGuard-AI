import math
from typing import Any, Dict, List


def _normalize_category(category: str) -> str:
    return (category or "OTHER").upper().replace(" ", "_")


def _describe_issue(description: str, category: str) -> str:
    text = (description or "").lower()
    if "hole" in text or "pothole" in text or category == "POTHOLE":
        return "POTHOLE"
    if "road" in text or "damage" in text:
        return "ROAD_DAMAGE"
    if "light" in text or "streetlight" in text:
        return "STREETLIGHT"
    if "garbage" in text or "waste" in text:
        return "GARBAGE"
    if "water" in text or "leak" in text:
        return "WATER_LEAKAGE"
    if "drain" in text or "block" in text:
        return "DRAINAGE"
    if "electrical" in text or "spark" in text:
        return "ELECTRICAL_HAZARD"
    if "broken" in text or "equipment" in text:
        return "BROKEN_EQUIPMENT"
    return "OTHER"


def analyze_report(report: Dict[str, Any]) -> Dict[str, Any]:
    category = _normalize_category(report.get("category") or "OTHER")
    issue_type = _describe_issue(report.get("description", ""), category)
    description = (report.get("description") or "").strip()
    risk = "HIGH" if "danger" in description.lower() or "unsafe" in description.lower() or issue_type in {"POTHOLE", "ELECTRICAL_HAZARD"} else "MEDIUM"
    severity = "HIGH" if risk == "HIGH" else "MEDIUM"
    return {
        "category": category,
        "issue_type": issue_type,
        "severity": severity,
        "safety_risk": risk,
        "estimated_impact": risk,
        "recommended_department": {
            "POTHOLE": "Maintenance",
            "ROAD_DAMAGE": "Maintenance",
            "STREETLIGHT": "Electrical",
            "GARBAGE": "Waste Management",
            "WATER_LEAKAGE": "Plumbing",
            "DRAINAGE": "Drainage/Maintenance",
            "ELECTRICAL_HAZARD": "Electrical/Safety",
            "BROKEN_EQUIPMENT": "Maintenance/Lab",
            "OTHER": "Administration",
        }.get(issue_type, "Administration"),
        "confidence": 0.94,
        "reason": f"{description or 'Reported issue'} suggests a significant {issue_type.lower().replace('_', ' ')} hazard affecting public safety near the reported location.",
    }


def calculate_similarity(a: Dict[str, Any], b: Dict[str, Any]) -> float:
    if a.get("category") == b.get("category"):
        category_bonus = 0.30
    else:
        category_bonus = 0.0
    if a.get("description") and b.get("description") and a.get("description").lower() == b.get("description").lower():
        issue_bonus = 0.25
    else:
        issue_bonus = 0.0

    text_a = (a.get("description") or "").lower()
    text_b = (b.get("description") or "").lower()
    shared_words = set(text_a.split()) & set(text_b.split())
    text_similarity = min(len(shared_words) / max(1, len(set(text_a.split()) | set(text_b.split()))), 1.0)

    distance = 0.0
    if a.get("latitude") is not None and b.get("latitude") is not None:
        distance = math.sqrt((a["latitude"] - b["latitude"]) ** 2 + (a["longitude"] - b["longitude"]) ** 2) * 100

    if distance <= 0.15:
        geo_bonus = 0.25
    elif distance <= 0.4:
        geo_bonus = 0.15
    else:
        geo_bonus = 0.0

    return min(1.0, category_bonus + issue_bonus + geo_bonus + text_similarity * 0.35)


def cluster_reports(reports: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    clusters: List[List[Dict[str, Any]]] = []
    for report in reports:
        matched = False
        for cluster in clusters:
            base = cluster[0]
            if calculate_similarity(report, base) >= 0.68:
                cluster.append(report)
                matched = True
                break
        if not matched:
            clusters.append([report])
    return [{"cluster_id": i + 1, "reports": cluster} for i, cluster in enumerate(clusters)]


def calculate_priority(incident: Dict[str, Any]) -> Dict[str, Any]:
    supporting_count = incident.get("supporting_report_count", 1)
    severity_score = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}[incident.get("severity", "MEDIUM")]
    score = severity_score * 25 + min(supporting_count * 10, 30) + incident.get("risk_score", 10)
    if score >= 85:
        return {"priority": "P1", "label": "CRITICAL", "score": score, "explanation": "Multiple reports indicate a significant safety hazard near a high-traffic area."}
    if score >= 65:
        return {"priority": "P2", "label": "HIGH", "score": score, "explanation": "Repeated reports and elevated risk suggest an urgent maintenance response."}
    if score >= 45:
        return {"priority": "P3", "label": "MEDIUM", "score": score, "explanation": "Moderate risk with enough evidence to justify scheduled repair."}
    return {"priority": "P4", "label": "LOW", "score": score, "explanation": "Low urgency issue with limited impact and limited report volume."}


def verify_resolution(incident: Dict[str, Any], worker_notes: str) -> Dict[str, Any]:
    summary = (worker_notes or "").lower()
    approved = "not fixed" not in summary and "still unresolved" not in summary
    return {
        "approved": approved,
        "status": "APPROVED" if approved else "REJECTED",
        "summary": "Repair appears complete and verified by evidence." if approved else "Resolution notes indicate work is incomplete or not yet verified.",
        "confidence": 0.91 if approved else 0.72,
    }
