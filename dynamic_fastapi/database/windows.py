"""Windows collections."""
from collections.abc import Mapping
from typing import Any

from dynamic_fastapi.database.collection import collection
from dynamic_fastapi.model.task_type import TaskTypeRegistry
from dynamic_fastapi.model.window import Window


@collection(Window, "windows")
class WindowCollection:
    """Collection for windows."""

    def from_doc(self, doc: Mapping[str, Any]) -> Window:
        """Parse the doc using the task type-specific window.

        :param doc: The window document.

        :returns: The parsed window document.
        """
        task_type = TaskTypeRegistry.task_type(doc["params"]["task_type"])
        return Window[task_type.params_model].parse_obj(doc)
