"""Department model."""

from sqlalchemy import Column, Integer, String
from app.models.database import Base


class Department(Base):
    """Department table - stores the 12 university departments."""

    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)

    def __repr__(self):
        return f"<Department(id={self.id}, name='{self.name}')>"
