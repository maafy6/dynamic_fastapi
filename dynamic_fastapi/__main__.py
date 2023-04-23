import logging

import click
import uvicorn

from dynamic_fastapi.app import app
from dynamic_fastapi.app.config import load_config


@click.command
@click.option("--config", "-c", type=click.Path(exists=True))
def main(config: str) -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[logging.StreamHandler()],
    )

    app_config = load_config(config)

    uvicorn_config = uvicorn.Config(app, **app_config.uvicorn.dict())
    uvicorn_server = uvicorn.Server(uvicorn_config)
    uvicorn_server.run()


if __name__ == "__main__":
    main()
