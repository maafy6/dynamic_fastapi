"""Base collection utilities."""
from collections.abc import Iterator, Mapping
from typing import Any, Generic, TypeVar

from motor.motor_asyncio import AsyncIOMotorDatabase

from dynamic_fastapi.model.base import DatabaseModel

_MT = TypeVar("_MT", bound=DatabaseModel)


class Collection(Generic[_MT]):
    """Model-based interface to a Mongo collection."""

    class Config:
        """Configuration for the collection."""

        collection_name: str
        """The name of the collection for this class."""
        model_class: type[_MT]
        """The model for documents in this collection."""

    def __init__(self, db: AsyncIOMotorDatabase):
        """Create a new collection.

        :param db: The database connection.
        """
        self.collection = db[self.Config.collection_name]

    def from_doc(self, doc: Mapping[str, Any]) -> _MT:
        """Parse a document to the model class.

        :param doc: The document from the database.

        :returns: The parsed document.
        """
        return self.Config.model_class.parse_obj(doc)

    async def find(self, *args, **kwargs) -> Iterator[_MT]:
        """Find documents matching the arguments.

        :param args: Positional arguments passed to find.
        :param kwargs: Keyword arguments passed to find.

        :yields: Parsed models of matching documents.
        """
        cursor = self.collection.find(*args, **kwargs)
        async for doc in cursor:
            yield self.from_doc(doc)

    async def insert_one(self, value: _MT) -> _MT:
        """Insert the document into the database.

        :param value: The value to insert.

        :returns: The inserted value. The returned value will have its `id`
            field set to the ID attached to the document on insertion.
        """
        result = await self.collection.insert_one(value.dict())
        if result.acknowledged:
            value.id = result.inserted_id
        return value


def collection(model: type[DatabaseModel], collection: str):
    """Class decorator for creating collections.

    :param model: The model class for the documents in the collection.
    :param collection: The name of the collection in the database.

    :returns: A Collection[model] class.
    """

    def _decorator(cls):
        class _Collection(cls, Collection[model]):
            class Config:
                collection_name = collection
                model_class = model

        _Collection.__name__ = cls.__name__

        return _Collection

    return _decorator
