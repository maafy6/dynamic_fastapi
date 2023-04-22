"""Tests for dynamic_fastapi.database.windows."""
from dynamic_fastapi.database.windows import WindowCollection
from dynamic_fastapi.model.window import Window


class TestTaskTypeCollection:
    """Tests for dynamic_fastapi.database.windows.WindowCollection."""

    def test_config(self) -> None:
        """Test dynamic_fastapi.database.windows.WindowCollection.Config."""
        assert WindowCollection.Config.collection_name == "windows"
        assert WindowCollection.Config.model_class == Window
