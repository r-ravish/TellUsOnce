"""Request actions API endpoint - department staff actions."""

import json
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.case import Case
from app.models.request import Request as RequestModel
from app.schemas.request import RequestActionInput
from app.services.audit_service import add_timeline_event, add_audit_log
from app.services.routing_service import _update_case_status
from app.api.cases import _serialize_request

logger = logging.getLogger(__name__)

router = APIRouter()

VALID_ACTIONS = {"accept", "complete", "note", "human_override"}
VALID_OVERRIDE_ACTIONS = {"approve", "route", "escalate"}


@router.post("/requests/{request_id}/action")
def request_action(
    request_id: int,
    action_input: RequestActionInput,
    db: Session = Depends(get_db),
):
    """
    Process a department staff action on a request.

    Supported actions:
    - accept: Department accepts/acknowledges the request
    - complete: Department marks the request as completed
    - note: Department adds a note to the request
    - human_override: Staff overrides the decision (approve/route/escalate only)
    """
    # Validate action
    if action_input.action not in VALID_ACTIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid action '{action_input.action}'. Valid actions: {', '.join(VALID_ACTIONS)}",
        )

    # Get request
    request_obj = db.query(RequestModel).filter(RequestModel.id == request_id).first()
    if not request_obj:
        raise HTTPException(status_code=404, detail=f"Request {request_id} not found")

    # Get parent case
    case = db.query(Case).filter(Case.id == request_obj.case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail=f"Case for request {request_id} not found")

    action = action_input.action

    if action == "accept":
        request_obj.status = "In Progress"
        add_timeline_event(
            db, case.id, "DEPARTMENT_ACCEPTED",
            f"{request_obj.department} accepted {request_obj.request_type}. {action_input.note}".strip(),
            request_obj.department,
        )
        add_audit_log(
            db, case.id, "DEPARTMENT_ACCEPTED",
            f"{request_obj.department} accepted request. Note: {action_input.note or 'N/A'}",
            request_id=request_obj.id,
        )

    elif action == "complete":
        request_obj.status = "Done"
        add_timeline_event(
            db, case.id, "DEPARTMENT_COMPLETED",
            f"{request_obj.department} completed {request_obj.request_type}. {action_input.note}".strip(),
            request_obj.department,
        )
        add_audit_log(
            db, case.id, "DEPARTMENT_COMPLETED",
            f"{request_obj.department} completed request. Note: {action_input.note or 'N/A'}",
            request_id=request_obj.id,
        )

    elif action == "note":
        add_timeline_event(
            db, case.id, "NOTE",
            f"{request_obj.department} note on {request_obj.request_type}: {action_input.note}",
            request_obj.department,
        )
        add_audit_log(
            db, case.id, "NOTE",
            f"Note added by {request_obj.department}: {action_input.note}",
            request_id=request_obj.id,
        )

    elif action == "human_override":
        if not action_input.override_action:
            raise HTTPException(
                status_code=400,
                detail="human_override action requires 'override_action' field (approve, route, escalate)",
            )
        if action_input.override_action not in VALID_OVERRIDE_ACTIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid override_action '{action_input.override_action}'. Valid: {', '.join(VALID_OVERRIDE_ACTIONS)}",
            )

        # Safety: human_override can NEVER decline/reject
        override = action_input.override_action
        if override == "approve":
            request_obj.final_action = "approve"
            request_obj.status = "Auto Approved"
        elif override == "route":
            request_obj.final_action = "route"
            request_obj.status = "Routed"
        elif override == "escalate":
            request_obj.final_action = "escalate"
            request_obj.status = "Escalated"

        add_timeline_event(
            db, case.id, "HUMAN_OVERRIDE",
            f"Human override on {request_obj.request_type}: {override}. {action_input.note}".strip(),
            request_obj.department,
        )
        add_audit_log(
            db, case.id, "HUMAN_OVERRIDE",
            f"Human override by {request_obj.department}: action changed to '{override}'. "
            f"Note: {action_input.note or 'N/A'}",
            request_id=request_obj.id,
        )

    # Update case status
    _update_case_status(db, case)
    db.commit()
    db.refresh(request_obj)

    return _serialize_request(request_obj)
