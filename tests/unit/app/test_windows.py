"""Tests for dynamic_fastapi.app.windows."""
from unittest.mock import patch

from dynamic_fastapi.app.windows import generate_routes, windows_api
from dynamic_fastapi.model.task_type import TaskType


class TestWindowsApi:
    """Tests for dynamic_fastapi.app.windows.windows_api."""

    def test_routes(self) -> None:
        """Test routes."""
        dummy_types = [TaskType(name="foo"), TaskType(name="bar")]
        with patch(
            "dynamic_fastapi.app.windows.TaskTypeRegistry.task_types",
            return_value=dummy_types,
        ), patch("dynamic_fastapi.model.task_type.globals", return_value={}):
            generate_routes()

        routes = {route.path: route.methods for route in windows_api.routes}
        assert routes == {
            "/windows/bar/create": {"POST"},
            "/windows/foo/create": {"POST"},
        }
