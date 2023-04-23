"""FastAPI application."""
from fastapi import FastAPI

from dynamic_fastapi.app.windows import windows_api

app = FastAPI()
app.include_router(windows_api)
