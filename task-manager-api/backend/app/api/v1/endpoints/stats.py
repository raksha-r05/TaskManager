from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import func, select

from ....core.dependencies import DbSession
from ....core.models import Task


router = APIRouter()


@router.get("/summary")
async def stats_summary(db: DbSession) -> dict[str, int]:
    total = await db.scalar(select(func.count()).select_from(Task))
    completed = await db.scalar(select(func.count()).select_from(Task).where(Task.is_completed.is_(True)))
    pending = (total or 0) - (completed or 0)
    return {"total": int(total or 0), "completed": int(completed or 0), "pending": int(pending)}


