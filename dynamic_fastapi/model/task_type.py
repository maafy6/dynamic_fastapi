"""Models for dynamic_fastapi."""
from collections.abc import Sequence
from logging import getLogger
from typing import Any

from pydantic import Field, ValidationError, constr, create_model, validator
from pydantic.fields import FieldInfo

from dynamic_fastapi.model.base import DatabaseModel
from dynamic_fastapi.model.extension import Extension
from dynamic_fastapi.model.window import WindowParams

_log = getLogger(__name__)


TaskTypeName = constr(regex=r"^[a-z][a-z0-9_]{0,14}[a-z0-9]$")
"""Task type string format.

The name for a task type must:
- Be between 2 and 16 characters long.
- Only contain lowercase letters, numbers, and underscores.
- Begin with a letter.
- Not end with an underscore.
"""


class TaskType(DatabaseModel):
    """Task type configuration.

    This model describes the confiugration of a task type.
    """

    name: TaskTypeName
    """The name of the task type."""
    extensions: dict[str, Any] = Field(default_factory=dict)
    """The extensions required for this task type."""

    @validator("extensions")
    def validate_extensions(
        cls, extensions: dict[str, Any]  # noqa: N805
    ) -> dict[str, Any]:
        """Validate that the extensions are valid.

        :param extensions: The provided extensions value.

        :returns: The extensions.

        :raises ValidationError: If one of the extensions is unable to be instantiated.
        """
        for ext_name, ext_args in extensions.items():
            try:
                ext_args = ext_args or {}
                Extension.extension(ext_name, **ext_args)
            except Exception as err:
                raise ValidationError(
                    f"Unable to create extension: {ext_name}"
                ) from err

        return extensions

    @property
    def params_model(self) -> type[WindowParams]:
        """Pydantic mode for the task type parameters."""

        kwargs = {"task_type": (str, FieldInfo(default=self.name))}
        for ext_name, ext_args in self.extensions.items():
            ext_args = ext_args or {}
            ext = Extension.extension(ext_name, **ext_args)
            kwargs.update(ext.field_definitions())

        model = create_model(
            f"{self.name.upper()}_WindowParams",
            __base__=WindowParams,
            __module__=self.__module__,
            **kwargs,
        )

        return model


class TaskTypeRegistry:
    """Registry of all saved task types."""

    __task_types__: dict[TaskTypeName, TaskType] = {}

    @classmethod
    def register(cls, task_type: TaskType) -> None:
        """Register a task type.

        :param task_type: The task type to register.
        """
        _log.info("Registering task type: %s", task_type.name)
        cls.__task_types__[task_type.name] = task_type

    @classmethod
    def task_type(cls, name: TaskTypeName) -> TaskType:
        """Retrieve a task type.

        :param name: The name of the task type.
        """
        return cls.__task_types__[name]

    @classmethod
    def task_types(cls) -> Sequence[TaskType]:
        """Retrieve all task types."""
        return cls.__task_types__.values()
