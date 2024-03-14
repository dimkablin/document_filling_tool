"""Endpoints for getting version information."""
from typing import Any
from fastapi import APIRouter
from ..version import __version__

router = APIRouter()


@router.get("/version", response_model=str)
async def version() -> Any:
    """Provide version information about the web service.

    \f
    Returns:
        VersionResponse: A json response containing the version number.
    """
    return __version__
