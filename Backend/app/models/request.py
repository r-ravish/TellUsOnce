"""Request model."""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.models.database import Base


class Request(Base):
    """Request table - individual needs extracted from a case."""

    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False, index=True)
    request_type = Column(String, nullable=False)
    department = Column(String, nullable=False, index=True)
    documents_mentioned = Column(Text, default="[]")  # JSON list stored as text
    days_requested = Column(Integer, default=0)
    ai_suggested_action = Column(String, nullable=True)  # approve, route, escalate
    ai_reason = Column(Text, nullable=True)
    final_action = Column(String, nullable=True)  # approve, route, escalate
    status = Column(String, default="New", index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    case = relationship("Case", back_populates="requests")
    audit_logs = relationship("AuditLog", back_populates="request", lazy="joined")

    def __repr__(self):
        return f"<Request(id={self.id}, type='{self.request_type}', dept='{self.department}', status='{self.status}')>"
