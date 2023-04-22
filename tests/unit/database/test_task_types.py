"""Tests for dynamic_fastapi.database.task_types."""
from dynamic_fastapi.database.task_types import TaskTypeCollection
from dynamic_fastapi.model.task_type import TaskType


class TestTaskTypeCollection:
    """Tests for dynamic_fastapi.database.task_types.TaskTypeCollection."""

    def test_config(self) -> None:
        """Test dynamic_fastapi.database.task_types.TaskTypeCollection.Config."""
        assert TaskTypeCollection.Config.collection_name == "task_types"
        assert TaskTypeCollection.Config.model_class == TaskType
