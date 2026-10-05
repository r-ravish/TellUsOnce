"""Decision engine - determines approve/route/escalate for each request."""

import logging
from app.services.policy_service import lookup_policy, check_documents

logger = logging.getLogger(__name__)


def decide(
    request_type: str,
    ai_suggested_action: str,
    documents_mentioned: list[str],
    days_requested: int,
    risk_flag: bool,
    confidence: float,
) -> dict:
    """
    Deterministic decision engine.

    AI SUGGESTS. PLAIN RULES DECIDE.

    A request may be AUTO-APPROVED only when ALL conditions are true:
    1. Policy explicitly allows auto approval.
    2. Requested days are within the allowed limit.
    3. Required documents are present.
    4. risk_flag == false.
    5. AI confidence >= 0.85.

    If ANY condition fails → ROUTE or ESCALATE.
    NEVER returns decline/reject.

    Returns:
        Dict with 'action', 'reason', and 'doc_check' keys.
    """
    policy = lookup_policy(request_type)

    # No policy found → route to Student Affairs
    if not policy:
        return {
            "action": "route",
            "reason": f"No policy found for request type '{request_type}'. Routing for human review.",
            "doc_check": {"documents_ok": True, "required": [], "missing": [], "mentioned": documents_mentioned},
        }

    # Always escalate counselling or policies marked always_escalate
    if policy.get("always_escalate", False):
        return {
            "action": "escalate",
            "reason": f"{policy['name']} always requires human/priority escalation per policy.",
            "doc_check": {"documents_ok": True, "required": [], "missing": [], "mentioned": documents_mentioned},
        }

    # Risk flag → escalate
    if risk_flag:
        return {
            "action": "escalate",
            "reason": "Risk flag detected. Escalating to human for safety review.",
            "doc_check": {"documents_ok": True, "required": [], "missing": [], "mentioned": documents_mentioned},
        }

    # Low confidence → escalate
    if confidence < 0.85:
        return {
            "action": "escalate",
            "reason": f"AI confidence ({confidence:.2f}) is below threshold (0.85). Escalating for human review.",
            "doc_check": {"documents_ok": True, "required": [], "missing": [], "mentioned": documents_mentioned},
        }

    # Policy does not allow auto approval → route
    if not policy.get("auto_approval", False):
        return {
            "action": "route",
            "reason": f"{policy['name']} policy does not allow auto-approval. Routing to {policy['department']}.",
            "doc_check": {"documents_ok": True, "required": [], "missing": [], "mentioned": documents_mentioned},
        }

    # Check days limit
    max_days = policy.get("max_days")
    if max_days is not None and days_requested > max_days:
        return {
            "action": "route",
            "reason": f"Requested {days_requested} days exceeds policy limit of {max_days} days. Routing to {policy['department']}.",
            "doc_check": {"documents_ok": True, "required": [], "missing": [], "mentioned": documents_mentioned},
        }

    # Check documents
    doc_check = check_documents(request_type, documents_mentioned)
    if not doc_check["documents_ok"]:
        return {
            "action": "route",
            "reason": f"Required documents missing: {', '.join(doc_check['missing'])}. Routing to {policy['department']}.",
            "doc_check": doc_check,
        }

    # ALL conditions pass → auto approve
    reason_parts = [
        f"{policy['name']} auto-approved."
    ]
    if max_days is not None:
        reason_parts.append(f"Requested {days_requested} days within limit of {max_days} days.")
    reason_parts.append("Required documents present.")
    reason_parts.append(f"AI confidence: {confidence:.2f}.")
    reason_parts.append("No risk flags.")

    return {
        "action": "approve",
        "reason": " ".join(reason_parts),
        "doc_check": doc_check,
    }
