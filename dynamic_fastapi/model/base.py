"""Base models for dynamic_fastapi."""
from typing import Any

from bson.objectid import ObjectId
from pydantic import BaseModel, Field


class PydanticObjectId(ObjectId):
    """Wrapper for BSON Object ID."""

    @classmethod
    def __get_validators__(cls):
        """Validators for PydanticObjectId."""
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        """Validate that the value is a valid object ID.

        :param v: The value to validate.

        :returns: The value as a BSON ObjectId.

        :raises ValueError: If the value cannot be instantiated as a valid
            ObjectId.
        """
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")

        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        """Modify the schema to accept this value as a string.

        :param field_schema: The schema for the field.
        """
        field_schema.update(type="string")


class DatabaseModel(BaseModel):
    """Base model for mongo documents."""

    class Config:
        # Required to allow setting the id by either `_id` or `id`.
        allow_population_by_field_name = True
        # Required to map the id field to a string when creating JSON.
        json_encoders = {ObjectId: str}
        # Encode enums as their values.
        use_enum_values = True

    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    """Mongo ID."""
