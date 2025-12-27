"""Core application configuration package.

Contains configuration, settings, and application dependencies.
"""

from app.core.config import settings
from app.core.lifespan_events import lifespan

__all__ = ["settings", "lifespan"]