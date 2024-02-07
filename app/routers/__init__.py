from app.core.log_route import LogRoute
from fastapi import APIRouter
from app.routers import (
    statistics,
    insta_client
)

api_router = APIRouter(route_class=LogRoute)
api_router.include_router(
    statistics.router,
    prefix="/statistics",
    tags=["statistics"]
)
api_router.include_router(
    insta_client.router,
    prefix="/insta_client",
    tags=["insta_client"]
)