"""Window models for dynamic_fastapi."""
from datetime import datetime
from enum import Enum
from typing import Generic, TypeVar

from pydantic import BaseModel, conlist
from pydantic.generics import GenericModel

from dynamic_fastapi.model.base import DatabaseModel


class WindowParams(BaseModel):
    """Window creation parameters model."""

    class Config:
        """Configuration for the parameters class."""

        use_enum_values = True

    task_type: str
    """The type of task."""
    start_time: datetime
    """The time to begin processing."""
    stop_time: datetime
    """The time to end processing."""
    datasources: conlist(str, min_items=1)
    """List of sources used to provide data."""


class WindowState(Enum):
    """State of a window."""

    OPEN = "open"
    """The window is open."""
    CANCELLED = "cancelled"
    """The window was cancelled by user action."""
    COMPLETE = "complete"
    """The window ran to completion."""


_WPT = TypeVar("_WPT", bound=WindowParams)


class Window(DatabaseModel, GenericModel, Generic[_WPT]):
    """Window model."""

    params: _WPT
    """Window creation parameters."""
    state: WindowState = WindowState.OPEN
    """Current window state."""
