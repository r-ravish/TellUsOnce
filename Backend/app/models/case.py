"""Case model."""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text
from sqlalchemy.orm import relationship
from app.models.database import Base


class Case(Base):
    """Case table - a student's joined-up case containing multiple requests."""

    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    student_reference = Column(String, nullable=False, index=True)
    original_story = Column(Text, nullable=False)
    masked_story = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    urgency = Column(String, default="medium")  # low, medium, high
    risk_flag = Column(Boolean, default=False)
    confidence = Column(Float, default=0.0)
    status = Column(String, default="New", index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    requests = relationship("Request", back_populates="case", lazy="joined")
    timeline = relationship(
        "Timeline", back_populates="case", lazy="joined", order_by="Timeline.created_at"
    )
    audit_logs = relationship(
        "AuditLog", back_populates="case", lazy="joined", order_by="AuditLog.created_at"
    )

    def __repr__(self):
        return f"<Case(id={self.id}, student='{self.student_reference}', status='{self.status}')>"
