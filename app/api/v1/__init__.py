"""API v1 routes aggregator.

Central place to include all v1 routers. main.py imports `api_router`
from here, so adding new routers only requires updating this file.
"""

from fastapi import APIRouter
from app.api.v1 import auth

api_router = APIRouter()
api_router.include_router(auth.router)
__all__ = ["api_router"]
