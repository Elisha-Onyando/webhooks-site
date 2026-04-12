from fastapi import APIRouter

from src.core.config import settings
from src.modules.webhooks.router import webhook_router, requests_router

api_router = APIRouter()
api_router.include_router(webhook_router, prefix=f"/api/{settings.api_version}")
api_router.include_router(requests_router)