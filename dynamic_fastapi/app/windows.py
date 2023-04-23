"""Windows routes for dynamic_fastapi."""
from logging import getLogger

from fastapi import APIRouter

from dynamic_fastapi.app.depends import WindowsDBDep
from dynamic_fastapi.model.window import Window, WindowParams

_log = getLogger(__name__)

windows_api = APIRouter(prefix="/windows")


@windows_api.post("/create")
async def create_window(params: WindowParams, windows_db: WindowsDBDep) -> Window:
    """Create a window.
    \f
    :param params: The window create parameters.
    :param windows_db: The windows database collection.

    :returns: The created window.
    """
    _log.info("Creating window with parameters: %s", params)
    window = await windows_db.insert_one(Window(params=params))
    return window
