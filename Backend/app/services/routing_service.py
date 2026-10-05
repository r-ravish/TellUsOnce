"""Routing service - handles approve, route, escalate actions and request management."""

import json
import logging
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.case import Case
from app.models.request import Request
from app.models.audit import Timeline, AuditLog
from app.services.policy_service import get_department_for_type

logger = logging.getLogger(__name__)


def approve_request(
    db: Session, request_obj: Request, case: Case, reason: str
) -> Request:
    """
    Approve a request. Verifies policy gate internally before approving.

    Args:
        db: Database session.
        request_obj: The request to approve.
        case: The parent case.
        reason: The reason for approval.

    Returns:
        Updated request.
    """
    request_obj.final_action = "approve"
    request_obj.status = "Auto Approved"

    # Update case status
    _update_case_status(db, case)

    # Timeline
    _add_timeline(
        db, case.id,
        "AUTO_APPROVED",
        f"{request_obj.request_type} auto-approved for {request_obj.department}.",
        request_obj.department,
    )

    # Audit
    _add_audit(
        db, case.id, request_obj.id,
        "AUTO_APPROVED",
        reason,
    )

    # Notify department
    _add_timeline(
        db, case.id,
        "DEPARTMENT_NOTIFIED",
        f"{request_obj.department} notified of approved request.",
        request_obj.department,
    )

    db.commit()
    return request_obj


def route_request(
    db: Session, request_obj: Request, case: Case, reason: str
) -> Request:
    """
    Route a request to the appropriate department.

    Args:
        db: Database session.
        request_obj: The request to route.
        case: The parent case.
        reason: The reason for routing.

    Returns:
        Updated request.
    """
    # Determine status based on reason
    if "documents missing" in reason.lower() or "required documents" in reason.lower():
        request_obj.status = "Needs Documents"
    else:
        request_obj.status = "Routed"

    request_obj.final_action = "route"

    _update_case_status(db, case)

    _add_timeline(
        db, case.id,
        "ROUTED",
        f"{request_obj.request_type} routed to {request_obj.department}. {reason}",
        request_obj.department,
    )

    _add_audit(
        db, case.id, request_obj.id,
        "ROUTED",
        reason,
    )

    db.commit()
    return request_obj


def escalate_to_human(
    db: Session, request_obj: Request, case: Case, reason: str
) -> Request:
    """
    Escalate a request to human review.

    Args:
        db: Database session.
        request_obj: The request to escalate.
        case: The parent case.
        reason: The reason for escalation.

    Returns:
        Updated request.
    """
    request_obj.final_action = "escalate"
    request_obj.status = "Escalated"

    _update_case_status(db, case)

    _add_timeline(
        db, case.id,
        "ESCALATED",
        f"{request_obj.request_type} escalated for human review at {request_obj.department}. {reason}",
        request_obj.department,
    )

    _add_audit(
        db, case.id, request_obj.id,
        "ESCALATED",
        reason,
    )

    db.commit()
    return request_obj


def execute_decision(
    db: Session, request_obj: Request, case: Case, decision: dict
) -> Request:
    """
    Execute a decision from the decision engine.

    Args:
        db: Database session.
        request_obj: The request.
        case: The parent case.
        decision: Dict with 'action' and 'reason'.

    Returns:
        Updated request.
    """
    action = decision["action"]
    reason = decision["reason"]

    if action == "approve":
        return approve_request(db, request_obj, case, reason)
    elif action == "escalate":
        return escalate_to_human(db, request_obj, case, reason)
    else:
        return route_request(db, request_obj, case, reason)


def _update_case_status(db: Session, case: Case):
    """Update the overall case status based on request statuses."""
    # Refresh to get latest request statuses
    db.refresh(case)
    statuses = [r.status for r in case.requests]

    if all(s in ("Auto Approved", "Done") for s in statuses):
        case.status = "Auto Approved" if all(s == "Auto Approved" for s in statuses) else "Done"
    elif any(s == "Escalated" for s in statuses):
        case.status = "Escalated"
    elif any(s == "Needs Documents" for s in statuses):
        case.status = "Needs Documents"
    elif any(s == "Routed" for s in statuses):
        case.status = "Routed"
    elif any(s == "In Progress" for s in statuses):
        case.status = "In Progress"
    else:
        case.status = "New"


def _add_timeline(
    db: Session, case_id: int, event_type: str, message: str, department: str | None = None
):
    """Add a timeline entry."""
    entry = Timeline(
        case_id=case_id,
        event_type=event_type,
        message=message,
        department=department,
    )
    db.add(entry)


def _add_audit(
    db: Session, case_id: int, request_id: int | None, event_type: str, details: str
):
    """Add an audit log entry."""
    entry = AuditLog(
        case_id=case_id,
        request_id=request_id,
        event_type=event_type,
        details=details,
    )
    db.add(entry)
