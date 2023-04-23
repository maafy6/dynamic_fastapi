"""Tests for dynamic_fastapi.app.windows."""
from dynamic_fastapi.app.windows import windows_api


class TestWindowsApi:
    """Tests for dynamic_fastapi.app.windows.windows_api."""

    def test_routes(self) -> None:
        """Test routes."""
        routes = {route.path: route.methods for route in windows_api.routes}
        assert routes == {
            "/windows/create": {"POST"},
        }
