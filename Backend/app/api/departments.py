"""Departments API endpoint."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.department import Department
from app.schemas.department import DepartmentResponse

router = APIRouter()


@router.get("/departments", response_model=list[DepartmentResponse])
def list_departments(db: Session = Depends(get_db)):
    """Return all 12 departments."""
    departments = db.query(Department).order_by(Department.id).all()
    return departments
