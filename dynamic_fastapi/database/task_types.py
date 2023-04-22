"""Task type collections."""
from dynamic_fastapi.database.collection import collection
from dynamic_fastapi.model.task_type import TaskType, TaskTypeRegistry


@collection(TaskType, "task_types")
class TaskTypeCollection:
    """Collection for task types."""

    pass


async def register_types_from_db(task_types_db: TaskTypeCollection) -> None:
    """Register the task types loaded in the database.

    :param task_types_db: The task type collection.
    """
    async for task_type in task_types_db.find():
        TaskTypeRegistry.register(task_type)
