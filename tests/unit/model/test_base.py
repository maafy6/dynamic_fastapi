"""Tests for dynamic_fastapi.model.base."""
import pytest
from bson.objectid import ObjectId

from dynamic_fastapi.model.base import DatabaseModel

from .. import ModelTest


class TestDatabaseModel(ModelTest[DatabaseModel]):
    """Tests for dynamic_fastapi.model.base.DatabaseModel."""

    @pytest.mark.parametrize("id_field", ["id", "_id"])
    def test_init_by_field(self, id_field: str) -> None:
        """"""
        kwargs = {id_field: "12345678901234567890abcd"}
        v = DatabaseModel(**kwargs)

        assert v.id == ObjectId("12345678901234567890abcd")
