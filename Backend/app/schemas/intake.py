"""Pydantic schemas for intake endpoint."""

from pydantic import BaseModel, Field


class IntakeRequest(BaseModel):
    """Schema for the student intake story submission."""

    student_reference: str = Field(
        ..., min_length=1, max_length=100, description="Student reference identifier"
    )
    story: str = Field(
        ..., min_length=10, max_length=10000, description="The student's story"
    )


class AIAnalysisNeed(BaseModel):
    """Schema for a single need identified by AI analysis."""

    request_type: str = Field(..., description="Type of request")
    documents_mentioned: list[str] = Field(default_factory=list)
    days_requested: int = Field(default=0, ge=0)
    suggested_action: str = Field(..., description="approve, route, or escalate")
    reason: str = Field(default="", description="Reason for the suggestion")


class AIAnalysisResponse(BaseModel):
    """Schema for validated AI analysis response."""

    summary: str = Field(..., description="Summary of the student's situation")
    urgency: str = Field(default="medium", description="low, medium, or high")
    risk_flag: bool = Field(default=False)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    needs: list[AIAnalysisNeed] = Field(default_factory=list)
