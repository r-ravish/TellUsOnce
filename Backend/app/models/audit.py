"""Timeline and AuditLog models."""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.models.database import Base


class Timeline(Base):
    """Timeline table - ordered events for a case."""

    __tablename__ = "timeline"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False, index=True)
    event_type = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    department = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    case = relationship("Case", back_populates="timeline")

    def __repr__(self):
        return f"<Timeline(id={self.id}, case={self.case_id}, event='{self.event_type}')>"


class AuditLog(Base):
    """AuditLog table - detailed audit trail for every decision."""

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False, index=True)
    request_id = Column(Integer, ForeignKey("requests.id"), nullable=True, index=True)
    event_type = Column(String, nullable=False, index=True)
    details = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    case = relationship("Case", back_populates="audit_logs")
    request = relationship("Request", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog(id={self.id}, case={self.case_id}, event='{self.event_type}')>"
