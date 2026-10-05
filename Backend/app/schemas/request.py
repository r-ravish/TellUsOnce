"""Pydantic schemas for request actions."""

from pydantic import BaseModel, Field


class RequestActionInput(BaseModel):
    """Schema for department staff actions on a request."""

    action: str = Field(
        ...,
        description="Action to perform: accept, complete, note, human_override",
    )
    note: str = Field(default="", description="Optional note for the action")
    override_action: str = Field(
        default="",
        description="For human_override: the new action (approve, route, escalate)",
    )


class RequestResponse(BaseModel):
    """Response schema for a request."""

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
