"""FastAPI application."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from dynamic_fastapi.app.config import get_config
from dynamic_fastapi.app.windows import generate_routes, windows_api
from dynamic_fastapi.database.task_types import (
    TaskTypeCollection, register_types_from_db
)


@asynccontextmanager
async def _lifespan(app: FastAPI) -> None:
    """Lifespan function for FastAPI application.

    Handles setup/teardown of the application.

    :param app: The FastAPI application.
    """
    app_config = get_config()

    client = AsyncIOMotorClient(app_config.mongo.host)
    database = client[app_config.mongo.database]
    task_types_db = TaskTypeCollection(database)
    await register_types_from_db(task_types_db)
    client.close()

    generate_routes()

    app.include_router(windows_api)

    yield


app = FastAPI(lifespan=_lifespan)
