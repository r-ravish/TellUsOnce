"""Pydantic schemas for departments."""

from pydantic import BaseModel


class DepartmentResponse(BaseModel):
    """Response schema for a department."""

    id: int
    name: str

    model_config = {"from_attributes": True}
