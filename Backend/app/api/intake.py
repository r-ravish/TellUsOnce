"""Intake API endpoint - the core story submission flow."""

import json
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.case import Case
from app.models.request import Request as RequestModel
from app.schemas.intake import IntakeRequest
from app.services.privacy import mask_pii
from app.services.ai_service import analyze_story
from app.services.policy_service import get_department_for_type
from app.services.decision_engine import decide
from app.services.routing_service import execute_decision
from app.services.audit_service import add_timeline_event, add_audit_log
from app.utils.demo_fallback import get_demo_fallback

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/intake")
def intake_story(intake: IntakeRequest, db: Session = Depends(get_db)):
    """
    Accept a student's story and process it through the full pipeline:

    1. Validate input
    2. Mask PII
    3. Send masked story to AI (or fallback)
    4. Get structured analysis
    5. Create case
    6. Create requests
    7. Check policies
    8. Check documents
    9. Run decision engine
    10. Approve/route/escalate
    11. Create timeline events
    12. Create audit logs
    13. Return complete case
    """
    try:
        # Step 1: Validate input (handled by Pydantic)

        # Step 2: Mask PII
        masked_story = mask_pii(intake.story)

        # Step 3 & 4: AI Analysis (try demo fallback first, then AI, then general fallback)
        analysis = get_demo_fallback(masked_story)
        if analysis is None:
            analysis = analyze_story(masked_story)

        # Step 5: Create case
        case = Case(
            student_reference=intake.student_reference,
            original_story=intake.story,
            masked_story=masked_story,
            summary=analysis.summary,
            urgency=analysis.urgency,
            risk_flag=analysis.risk_flag,
            confidence=analysis.confidence,
            status="New",
        )
        db.add(case)
        db.flush()  # Get case.id

        # Timeline: Case created
        add_timeline_event(
            db, case.id, "CASE_CREATED",
            f"Case created for student {intake.student_reference}."
        )

        # Audit: AI analysis
        add_audit_log(
            db, case.id, "AI_ANALYSIS",
            f"AI analysis completed. Summary: {analysis.summary}. "
            f"Urgency: {analysis.urgency}. Risk: {analysis.risk_flag}. "
            f"Confidence: {analysis.confidence:.2f}. "
            f"Identified {len(analysis.needs)} need(s)."
        )

        # Timeline: AI analysis
        add_timeline_event(
            db, case.id, "AI_ANALYSIS",
            f"AI analysis completed. Identified {len(analysis.needs)} need(s)."
        )

        # Step 6-10: Process each need
        for need in analysis.needs:
            # Get department from policy (or use AI suggestion)
            department = get_department_for_type(need.request_type)

            # Create request
            request_obj = RequestModel(
                case_id=case.id,
                request_type=need.request_type,
                department=department,
                documents_mentioned=json.dumps(need.documents_mentioned),
                days_requested=need.days_requested,
                ai_suggested_action=need.suggested_action,
                ai_reason=need.reason,
            )
            db.add(request_obj)
            db.flush()  # Get request_obj.id

            # Audit: Document check
            from app.services.policy_service import check_documents
            doc_check = check_documents(need.request_type, need.documents_mentioned)
            add_audit_log(
                db, case.id, "DOCUMENT_CHECK",
                f"Document check for {need.request_type}: "
                f"Required: {doc_check['required']}. "
                f"Mentioned: {doc_check['mentioned']}. "
                f"Missing: {doc_check['missing']}. "
                f"OK: {doc_check['documents_ok']}.",
                request_id=request_obj.id,
            )

            # Step 9: Run decision engine
            decision = decide(
                request_type=need.request_type,
                ai_suggested_action=need.suggested_action,
                documents_mentioned=need.documents_mentioned,
                days_requested=need.days_requested,
                risk_flag=analysis.risk_flag,
                confidence=analysis.confidence,
            )

            # Step 10: Execute decision (approve/route/escalate)
            execute_decision(db, request_obj, case, decision)

        # Final commit
        db.commit()
        db.refresh(case)

        # Build response
        from app.api.cases import _serialize_case, _serialize_request, _serialize_timeline, _serialize_audit
        result = _serialize_case(case)
        result["requests"] = [_serialize_request(r) for r in case.requests]
        result["timeline"] = [_serialize_timeline(t) for t in case.timeline]
        result["audit_logs"] = [_serialize_audit(a) for a in case.audit_logs]

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Intake processing failed: {e}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the student's story. Please try again.",
        )
