from __future__ import annotations

from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, Query, status, Response
from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ....core.dependencies import DbSession
from ....core.models import Task
from ....core.schemas import TaskCreate, TaskOut, TaskUpdate


router = APIRouter()


@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(payload: TaskCreate, db: DbSession) -> TaskOut:
    task = Task(**payload.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return TaskOut.model_validate(task)


@router.get("/", response_model=list[TaskOut])
async def list_tasks(
    db: DbSession,
    q: str | None = None,
    is_completed: bool | None = None,
    min_priority: int | None = Query(None, ge=0),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> list[TaskOut]:
    stmt: Select[tuple[Task]] = select(Task)
    if q:
        stmt = stmt.where(func.lower(Task.title).contains(q.lower()))
    if is_completed is not None:
        stmt = stmt.where(Task.is_completed == is_completed)
    if min_priority is not None:
        stmt = stmt.where(Task.priority >= min_priority)
    stmt = stmt.limit(limit).offset(offset)
    rows = (await db.execute(stmt)).scalars().all()
    return [TaskOut.model_validate(t) for t in rows]


@router.get("/{task_id}", response_model=TaskOut)
async def get_task(task_id: int, db: DbSession) -> TaskOut:
    task = (await db.execute(select(Task).where(Task.id == task_id))).scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return TaskOut.model_validate(task)


@router.put("/{task_id}", response_model=TaskOut)
async def update_task(task_id: int, payload: TaskUpdate, db: DbSession) -> TaskOut:
    task = (await db.execute(select(Task).where(Task.id == task_id))).scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    await db.commit()
    await db.refresh(task)
    return TaskOut.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_task(task_id: int, db: DbSession) -> Response:
    task = (await db.execute(select(Task).where(Task.id == task_id))).scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    await db.delete(task)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


