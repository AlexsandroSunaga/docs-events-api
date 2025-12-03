from fastapi import APIRouter

from src.api.routes import events, integrations

api_router = APIRouter()
api_router.include_router(events.router)
api_router.include_router(integrations.router)

