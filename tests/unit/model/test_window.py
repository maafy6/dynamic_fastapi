"""Tests for dynamic_fastapi.model.window."""
from dynamic_fastapi.model.window import Window, WindowParams

from .. import ModelTest


class TestWindow(ModelTest[Window]):
    """Tests for dynamic_fastapi.model.window.Window."""

    __required_fields__ = ["params"]


class TestWindowParams(ModelTest[WindowParams]):
    """Tests for dynamic_fastapi.model.window.WindowParams."""

    __required_fields__ = ["task_type", "start_time", "stop_time", "datasources"]
