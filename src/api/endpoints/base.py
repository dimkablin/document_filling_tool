"""Endpoints for getting version information."""
from typing import Any
from fastapi import APIRouter
from ..version import __version__

base_router = APIRouter()


@base_router.get("/version", response_model=str)
async def version() -> Any:
    """Provide version information about the web service.

    \f
    Returns:
        VersionResponse: A json response containing the version number.
    """
    return __version__
