"""Tests for dynamic_fastapi.model.task_type."""
import pytest
from pydantic import StrRegexError

from dynamic_fastapi.model.task_type import TaskType, TaskTypeName

from .. import ModelTest


class TestTaskTypeName:
    """Tests for dynamic_fastapi.model.task_type.TaskTypeName."""

    @pytest.mark.parametrize(
        ("input", "valid"),
        [
            ("a_1", True),
            ("A1", False),
            ("a1", True),
            ("a", False),
            ("a" * 16, True),
            ("a" * 17, False),
            ("1_a", False),
            ("a-1", False),
            ("a_", False),
        ],
    )
    def test_validate(self, input: str, valid: bool) -> None:
        """Ensure the name"""
        try:
            TaskTypeName.validate(input)
            assert valid, f"Expected {input} to be valid."
        except StrRegexError:
            assert not valid, f"Expected {input} to be invalid."


class TestTaskType(ModelTest[TaskType]):
    """Tests for dynamic_fastapi.model.task_type.TaskType."""

    __required_fields__ = ["name"]

    def test_params_model(self) -> None:
        """Test params_model."""
        task_type = TaskType(
            name="foo",
            extensions={
                "symbol_set": None,
                "keynonce": {"key_len": 12, "nonce_len": 12},
            },
        )

        model = task_type.params_model

        assert model.__fields__.keys() == {
            "task_type",
            "start_time",
            "stop_time",
            "datasources",
            "symbol_set",
            "key",
            "nonce",
        }

        assert model.__fields__["task_type"].default == "foo"
