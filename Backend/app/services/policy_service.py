"""Policy service - deterministic policy lookup and enforcement."""

import json
import os
from pathlib import Path


# Load policies from JSON file
_POLICIES_PATH = Path(__file__).parent.parent / "data" / "policies.json"

_policies: dict = {}


def _load_policies() -> dict:
    """Load policies from the JSON file."""
    global _policies
    if not _policies:
        with open(_POLICIES_PATH, "r") as f:
            _policies = json.load(f)
    return _policies


def lookup_policy(request_type: str) -> dict | None:
    """
    Look up the policy for a given request type.

    Args:
        request_type: The type of request (e.g., 'fee_extension').

    Returns:
        The policy dict, or None if not found.
    """
    policies = _load_policies()
    return policies.get(request_type)


def get_department_for_type(request_type: str) -> str:
    """
    Get the department name for a request type.

    Args:
        request_type: The type of request.

    Returns:
        Department name, or 'Student Affairs' as fallback.
    """
    policy = lookup_policy(request_type)
    if policy:
        return policy.get("department", "Student Affairs")
    return "Student Affairs"


def check_documents(
    request_type: str, documents_mentioned: list[str]
) -> dict:
    """
    Check if required documents are present for a request type.

    Args:
        request_type: The type of request.
        documents_mentioned: List of documents the student mentioned.

    Returns:
        Dict with 'documents_ok', 'required', and 'missing' keys.
    """
    policy = lookup_policy(request_type)
    if not policy:
        return {
            "documents_ok": True,
            "required": [],
            "missing": [],
            "mentioned": documents_mentioned,
        }

    required = policy.get("required_documents", [])
    if not required:
        return {
            "documents_ok": True,
            "required": required,
            "missing": [],
            "mentioned": documents_mentioned,
        }

    # Check if any mentioned document matches a required document
    mentioned_lower = [d.lower().strip() for d in documents_mentioned]
    missing = []
    for req_doc in required:
        # Check if the required doc (or part of it) appears in mentioned docs
        found = False
        for mentioned in mentioned_lower:
            if req_doc.lower() in mentioned or mentioned in req_doc.lower():
                found = True
                break
        if not found:
            missing.append(req_doc)

    # If ANY required document is matched, consider docs ok
    # (student may have one of the acceptable documents)
    documents_ok = len(missing) < len(required)

    return {
        "documents_ok": documents_ok,
        "required": required,
        "missing": missing,
        "mentioned": documents_mentioned,
    }


def reload_policies():
    """Force reload policies from disk (useful for testing)."""
    global _policies
    _policies = {}
    _load_policies()
