"""Windows routes for dynamic_fastapi."""
from logging import getLogger

from fastapi import APIRouter

from dynamic_fastapi.app.depends import WindowsDBDep
from dynamic_fastapi.model.task_type import TaskType, TaskTypeRegistry
from dynamic_fastapi.model.window import Window

_log = getLogger(__name__)

windows_api = APIRouter(prefix="/windows")


def generate_routes() -> None:
    """Generate routes for windows_api."""
    window_types = None
    for task_type in TaskTypeRegistry.task_types():
        _generate_routes(task_type)
        if window_types is None:
            window_types = Window[task_type.params_model]
        else:
            window_types = window_types | Window[task_type.params_model]

    @windows_api.get("")
    async def list_windows(windows_db: WindowsDBDep) -> list[window_types]:
        """Return the list of windows."""
        return [window async for window in windows_db.find()]


def _generate_routes(task_type: TaskType) -> None:
    response_model = Window[task_type.params_model]

    @windows_api.post(f"/{task_type.name}/create")
    async def create_window(
        params: task_type.params_model, windows_db: WindowsDBDep
    ) -> response_model:
        """Create a window.
        \f
        :param params: The window create parameters.
        :param windows_db: The windows database collection.

        :returns: The created window.
        """
        _log.info("Creating %s window with parameters: %s", task_type.name, params)
        window = await windows_db.insert_one(response_model(params=params))
        return window
