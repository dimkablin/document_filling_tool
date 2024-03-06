"""The main APIRouter is defined to include all the sub routers from each
module inside the API folder"""
from fastapi import APIRouter
from .base import base_router
# TODO: import your modules here.

api_router = APIRouter()
api_router.include_router(base_router, tags=["base"])
# TODO: include the routers from other modules
