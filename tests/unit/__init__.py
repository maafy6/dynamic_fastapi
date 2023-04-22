"""Unit tests for dynamic_fastapi."""
from typing import Generic, TypeVar

from pydantic import BaseModel

_MT = TypeVar("_MT", bound=BaseModel)


class ModelTest(Generic[_MT]):
    """Base class for Pydantic model tests."""

    __required_fields__: list[str] = []
    """A list of fields required to construct the model."""

    def test_required_fields(self) -> None:
        """Verify the list of required fields is as expected."""
        required = {
            name for name, field in self.model.__fields__.items() if field.required
        }

        assert required == set(self.__required_fields__)

    @property
    def model(self) -> type[_MT]:
        """The model this class is testing."""
        return self.__class__.__orig_bases__[0].__args__[0]
