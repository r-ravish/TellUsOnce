"""Demo reset and gaps API endpoints."""

import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.database import get_db
from app.models.case import Case
from app.models.request import Request as RequestModel
from app.data.seed_data import reset_database, DEMO_STORIES
from app.api.intake import intake_story
from app.schemas.intake import IntakeRequest

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/demo/reset")
def demo_reset(db: Session = Depends(get_db)):
    """
    Reset the database to seeded demo data.

    1. Drops all tables
    2. Recreates tables
    3. Seeds departments
    4. Processes demo stories through the intake pipeline
    """
    # Reset database
    reset_database(db)

    # Process demo stories through intake
    results = []
    for demo in DEMO_STORIES:
        try:
            intake_req = IntakeRequest(
                student_reference=demo["student_reference"],
                story=demo["story"],
            )
            result = intake_story(intake_req, db)
            results.append({
                "student_reference": demo["student_reference"],
                "status": "processed",
                "case_id": result.get("id"),
            })
        except Exception as e:
            logger.error(f"Error processing demo story: {e}")
            results.append({
                "student_reference": demo["student_reference"],
                "status": "error",
                "error": str(e),
            })

    return {
        "message": "Demo database reset complete",
        "demo_cases": results,
    }


@router.get("/gaps")
def get_gaps(db: Session = Depends(get_db)):
    """
    Return system-level gaps and issues.

    - Unowned requests (no final action)
    - Stuck requests (routed but not accepted)
    - Cases involving 3+ departments
    - Escalated cases
    - Requests waiting for documents
    """
    # Unowned requests (still New status)
    unowned = (
        db.query(RequestModel)
        .filter(RequestModel.status == "New")
        .all()
    )

    # Stuck requests (Routed but not In Progress or Done)
    stuck = (
        db.query(RequestModel)
        .filter(RequestModel.status == "Routed")
        .all()
    )

    # Cases involving 3+ departments
    multi_dept_cases = []
    cases = db.query(Case).all()
    for case in cases:
        departments = set(r.department for r in case.requests)
        if len(departments) >= 3:
            multi_dept_cases.append({
                "case_id": case.id,
                "student_reference": case.student_reference,
                "departments": list(departments),
                "department_count": len(departments),
            })

    # Escalated cases
    escalated = (
        db.query(Case)
        .filter(Case.status == "Escalated")
        .all()
    )

    # Requests waiting for documents
    needs_docs = (
        db.query(RequestModel)
        .filter(RequestModel.status == "Needs Documents")
        .all()
    )

    return {
        "unowned_requests": [
            {
                "request_id": r.id,
                "case_id": r.case_id,
                "request_type": r.request_type,
                "department": r.department,
            }
            for r in unowned
        ],
        "stuck_requests": [
            {
                "request_id": r.id,
                "case_id": r.case_id,
                "request_type": r.request_type,
                "department": r.department,
                "status": r.status,
            }
            for r in stuck
        ],
        "multi_department_cases": multi_dept_cases,
        "escalated_cases": [
            {
                "case_id": c.id,
                "student_reference": c.student_reference,
                "status": c.status,
                "urgency": c.urgency,
            }
            for c in escalated
        ],
        "needs_documents": [
            {
                "request_id": r.id,
                "case_id": r.case_id,
                "request_type": r.request_type,
                "department": r.department,
            }
            for r in needs_docs
        ],
        "summary": {
            "total_unowned": len(unowned),
            "total_stuck": len(stuck),
            "total_multi_dept": len(multi_dept_cases),
            "total_escalated": len(escalated),
            "total_needs_docs": len(needs_docs),
        },
    }
