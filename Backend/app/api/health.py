"""Health check endpoint."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    """Return backend health status."""
    return {
        "status": "healthy",
        "service": "Tell Us Once Backend",
        "version": "1.0.0",
    }
