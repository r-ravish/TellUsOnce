"""Cases API endpoints."""

import json
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.case import Case
from app.schemas.case import (
    CaseResponse,
    CaseDetailResponse,
    CaseDepartmentView,
    RequestInCase,
    TimelineResponse,
    AuditLogResponse,
)

router = APIRouter()


def _serialize_request(req) -> dict:
    """Serialize a request model to a dict for the schema."""
    docs = req.documents_mentioned
    if isinstance(docs, str):
        try:
            docs = json.loads(docs)
        except (json.JSONDecodeError, TypeError):
            docs = []

    return {
        "id": req.id,
        "case_id": req.case_id,
        "request_type": req.request_type,
        "department": req.department,
        "documents_mentioned": docs,
        "days_requested": req.days_requested,
        "ai_suggested_action": req.ai_suggested_action,
        "ai_reason": req.ai_reason,
        "final_action": req.final_action,
        "status": req.status,
        "created_at": str(req.created_at) if req.created_at else "",
        "updated_at": str(req.updated_at) if req.updated_at else "",
    }


def _serialize_timeline(t) -> dict:
    """Serialize a timeline model to a dict."""
    return {
        "id": t.id,
        "case_id": t.case_id,
        "event_type": t.event_type,
        "message": t.message,
        "department": t.department,
        "created_at": str(t.created_at) if t.created_at else "",
    }


def _serialize_audit(a) -> dict:
    """Serialize an audit log model to a dict."""
    return {
        "id": a.id,
        "case_id": a.case_id,
        "request_id": a.request_id,
        "event_type": a.event_type,
        "details": a.details,
        "created_at": str(a.created_at) if a.created_at else "",
    }


def _serialize_case(case) -> dict:
    """Serialize a case model to a dict."""
    return {
        "id": case.id,
        "student_reference": case.student_reference,
        "original_story": case.original_story,
        "masked_story": case.masked_story,
        "summary": case.summary,
        "urgency": case.urgency,
        "risk_flag": case.risk_flag,
        "confidence": case.confidence,
        "status": case.status,
        "created_at": str(case.created_at) if case.created_at else "",
        "updated_at": str(case.updated_at) if case.updated_at else "",
    }


@router.get("/cases")
def list_cases(db: Session = Depends(get_db)):
    """Return all cases."""
    cases = db.query(Case).order_by(Case.created_at.desc()).all()
    result = []
    for case in cases:
        data = _serialize_case(case)
        data["requests"] = [_serialize_request(r) for r in case.requests]
        result.append(data)
    return result


@router.get("/cases/{case_id}")
def get_case(
    case_id: int,
    department: str | None = Query(default=None, description="Filter by department"),
    db: Session = Depends(get_db),
):
    """
    Return a specific case.

    If department query parameter is provided, returns a filtered view
    showing only information relevant to that department.
    """
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found")

    if department:
        # Department-filtered view - minimal info, no original story
        dept_requests = [
            _serialize_request(r) for r in case.requests if r.department == department
        ]
        dept_timeline = [
            _serialize_timeline(t)
            for t in case.timeline
            if t.department == department or t.department is None
        ]

        return {
            "id": case.id,
            "student_reference": case.student_reference,
            "masked_story": case.masked_story,
            "summary": case.summary,
            "urgency": case.urgency,
            "risk_flag": case.risk_flag,
            "status": case.status,
            "created_at": str(case.created_at) if case.created_at else "",
            "requests": dept_requests,
            "timeline": dept_timeline,
        }

    # Full case detail
    data = _serialize_case(case)
    data["requests"] = [_serialize_request(r) for r in case.requests]
    data["timeline"] = [_serialize_timeline(t) for t in case.timeline]
    data["audit_logs"] = [_serialize_audit(a) for a in case.audit_logs]
    return data
