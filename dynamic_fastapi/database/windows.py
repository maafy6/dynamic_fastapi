"""Windows collections."""
from dynamic_fastapi.database.collection import collection
from dynamic_fastapi.model.window import Window


@collection(Window, "windows")
class WindowCollection:
    """Collection for windows."""

    pass
