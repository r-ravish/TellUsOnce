"""Pydantic schemas for case responses."""

from pydantic import BaseModel


class TimelineResponse(BaseModel):
    """Response schema for a timeline entry."""

    id: int
    case_id: int
    event_type: str
    message: str
    department: str | None = None
    created_at: str

    model_config = {"from_attributes": True}


class AuditLogResponse(BaseModel):
    """Response schema for an audit log entry."""

    id: int
    case_id: int
    request_id: int | None = None
    event_type: str
    details: str
    created_at: str

    model_config = {"from_attributes": True}


class RequestInCase(BaseModel):
    """Response schema for a request within a case."""

    id: int
    case_id: int
    request_type: str
    department: str
    documents_mentioned: list[str] = []
    days_requested: int = 0
    ai_suggested_action: str | None = None
    ai_reason: str | None = None
    final_action: str | None = None
    status: str = "New"
    created_at: str
    updated_at: str

    model_config = {"from_attributes": True}


class CaseResponse(BaseModel):
    """Response schema for a case."""

    id: int
    student_reference: str
    original_story: str
    masked_story: str
    summary: str | None = None
    urgency: str = "medium"
    risk_flag: bool = False
    confidence: float = 0.0
    status: str = "New"
    created_at: str
    updated_at: str

    model_config = {"from_attributes": True}


class CaseDetailResponse(BaseModel):
    """Response schema for a case with full details."""

    id: int
    student_reference: str
    original_story: str
    masked_story: str
    summary: str | None = None
    urgency: str = "medium"
    risk_flag: bool = False
    confidence: float = 0.0
    status: str = "New"
    created_at: str
    updated_at: str
    requests: list[RequestInCase] = []
    timeline: list[TimelineResponse] = []
    audit_logs: list[AuditLogResponse] = []

    model_config = {"from_attributes": True}


class CaseDepartmentView(BaseModel):
    """Minimal case view for a specific department."""

    id: int
    student_reference: str
    masked_story: str
    summary: str | None = None
    urgency: str = "medium"
    risk_flag: bool = False
    status: str = "New"
    created_at: str
    requests: list[RequestInCase] = []
    timeline: list[TimelineResponse] = []

    model_config = {"from_attributes": True}
