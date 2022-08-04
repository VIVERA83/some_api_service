from fastapi import FastAPI

from src.core.config import settings
from src.api.v1.clients import client_router

app = FastAPI(
    title=settings.app.app_name,
    docs_url=settings.app.docs_url,
    openapi_url=settings.app.openapi_url,
    description=settings.app.description,
    version=settings.app.version,
)

app.include_router(client_router, prefix="/api/clients")
