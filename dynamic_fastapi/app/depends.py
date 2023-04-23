from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from dynamic_fastapi.app.config import get_config
from dynamic_fastapi.database.windows import WindowCollection


def _database() -> AsyncIOMotorDatabase:
    """Provide a connection to the database.

    :yields: A connection to the database.
    """
    app_config = get_config()
    client = AsyncIOMotorClient(app_config.mongo.host)
    db = client[app_config.mongo.database]
    yield db
    client.close()


DatabaseDep = Annotated[AsyncIOMotorDatabase, Depends(_database)]
"""Database connection dependency."""


def _windows_collection(db: DatabaseDep) -> WindowCollection:
    """Provide a windows collection interface.

    :param db: The database connection.

    :yields: A windows collection instance.
    """
    yield WindowCollection(db)


WindowsDBDep = Annotated[WindowCollection, Depends(_windows_collection)]
"""Windows database collection dependency."""
