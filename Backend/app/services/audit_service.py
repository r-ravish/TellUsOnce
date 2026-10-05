"""Audit service - helpers for creating audit and timeline entries."""

from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.audit import Timeline, AuditLog


def add_timeline_event(
    db: Session,
    case_id: int,
    event_type: str,
    message: str,
    department: str | None = None,
) -> Timeline:
    """
    Add a timeline event for a case.

    Args:
        db: Database session.
        case_id: The case ID.
        event_type: Type of event.
        message: Human-readable message.
        department: Optional department name.

    Returns:
        Created Timeline entry.
    """
    entry = Timeline(
        case_id=case_id,
        event_type=event_type,
        message=message,
        department=department,
    )
    db.add(entry)
    db.flush()
    return entry


def add_audit_log(
    db: Session,
    case_id: int,
    event_type: str,
    details: str,
    request_id: int | None = None,
) -> AuditLog:
    """
    Add an audit log entry.

    Args:
        db: Database session.
        case_id: The case ID.
        event_type: Type of audit event.
        details: Detailed information about the event.
        request_id: Optional request ID.

    Returns:
        Created AuditLog entry.
    """
    entry = AuditLog(
        case_id=case_id,
        request_id=request_id,
        event_type=event_type,
        details=details,
    )
    db.add(entry)
    db.flush()
    return entry
