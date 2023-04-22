"""Tests for dynamic_fastapi.model."""
import dynamic_fastapi.model


def test_exports() -> None:
    """Test the package exports the expected members."""
    assert set(dynamic_fastapi.model.__all__) == {
        "Extension",
        "TaskType",
        "Window",
        "WindowParams",
    }
