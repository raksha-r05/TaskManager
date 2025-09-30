from fastapi import APIRouter

from .endpoints import tasks, stats


api_router = APIRouter()
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(stats.router, prefix="/stats", tags=["stats"])


