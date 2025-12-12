"""API v1 routers package.

Contains all route handlers for API v1 endpoints.
"""

from app.api.v1.routers.users import router as users_router

__all__ = ["users_router"]
