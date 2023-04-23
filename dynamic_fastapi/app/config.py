"""Configuration models for the application."""
from pydantic import BaseModel
from yaml import safe_load as load_yaml

_app_config: "AppConfig" = None
"""Global application config."""


class MongoConfig(BaseModel):
    """Configuration for mongo."""

    host: str
    """The host string to connect to mongo db."""
    database: str
    """The name of the mongo database."""


class UvicornConfig(BaseModel):
    """Configuration for uvicorn server."""

    port: int
    """The port to serve."""
    log_level: str
    """The level of logs to allow."""


class AppConfig(BaseModel):
    """Main application config."""

    uvicorn: UvicornConfig
    mongo: MongoConfig


def get_config() -> AppConfig:
    """The global application configuration."""
    return _app_config


def load_config(config_file: str) -> AppConfig:
    """Set the global application configuration from the config file.

    :param config_file: The config file for the application.
    """
    global _app_config
    with open(config_file) as fp:
        _app_config = AppConfig.parse_obj(load_yaml(fp))

    return _app_config
