"""Tests for dynamic_fastapi.app.config."""
from dynamic_fastapi.app.config import AppConfig, MongoConfig, UvicornConfig

from .. import ModelTest


class TestAppConfig(ModelTest[AppConfig]):
    """Tests for dynamic_fastapi.app.config.AppConfig."""

    __required_fields__ = {"mongo", "uvicorn"}


class TestMongoConfig(ModelTest[MongoConfig]):
    """Tests for dynamic_fastapi.app.config.MongoConfig."""

    __required_fields__ = {"database", "host"}


class TestUvicornConfig(ModelTest[UvicornConfig]):
    """Tests for dynamic_fastapi.app.config.UvicornConfig."""

    __required_fields__ = {"port", "log_level"}
