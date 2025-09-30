from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from sqlalchemy import Boolean, DateTime, Integer, String, Text, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


DB_PATH = Path(__file__).resolve().parent.parent / "todo.db"
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"


class Base(DeclarativeBase):
	pass


class Task(Base):
	__tablename__ = "tasks"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	title: Mapped[str] = mapped_column(String(255), nullable=False)
	description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
	is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
	priority: Mapped[int] = mapped_column(Integer, default=0)
	due_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
	updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


engine = create_async_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


class TaskBase(BaseModel):
	title: str
	description: Optional[str] = None
	is_completed: Optional[bool] = False
	priority: Optional[int] = 0
	due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
	pass


class TaskUpdate(BaseModel):
	title: Optional[str] = None
	description: Optional[str] = None
	is_completed: Optional[bool] = None
	priority: Optional[int] = None
	due_date: Optional[datetime] = None


class TaskOut(TaskBase):
	id: int
	created_at: datetime
	updated_at: datetime

	class Config:
		from_attributes = True


app = FastAPI(title="v1 ToDo List API")


@app.on_event("startup")
async def on_startup() -> None:
	DB_PATH.parent.mkdir(parents=True, exist_ok=True)
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)


@app.get("/", tags=["health"])  # simple check
async def root() -> dict[str, str]:
	return {"status": "ok"}


@app.post("/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED, tags=["tasks"])
async def create_task(payload: TaskCreate) -> TaskOut:
	async with SessionLocal() as session:
		task = Task(**payload.model_dump())
		session.add(task)
		await session.commit()
		await session.refresh(task)
		return TaskOut.model_validate(task)


@app.get("/tasks", response_model=list[TaskOut], tags=["tasks"])
async def list_tasks() -> list[TaskOut]:
	async with SessionLocal() as session:
		rows = (await session.execute(select(Task))).scalars().all()
		return [TaskOut.model_validate(t) for t in rows]


@app.get("/tasks/{task_id}", response_model=TaskOut, tags=["tasks"])
async def get_task(task_id: int) -> TaskOut:
	async with SessionLocal() as session:
		task = (await session.execute(select(Task).where(Task.id == task_id))).scalar_one_or_none()
		if task is None:
			raise HTTPException(status_code=404, detail="Task not found")
		return TaskOut.model_validate(task)


@app.put("/tasks/{task_id}", response_model=TaskOut, tags=["tasks"])
async def update_task(task_id: int, payload: TaskUpdate) -> TaskOut:
	async with SessionLocal() as session:
		task = (await session.execute(select(Task).where(Task.id == task_id))).scalar_one_or_none()
		if task is None:
			raise HTTPException(status_code=404, detail="Task not found")
		for key, value in payload.model_dump(exclude_unset=True).items():
			setattr(task, key, value)
		await session.commit()
		await session.refresh(task)
		return TaskOut.model_validate(task)


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response, tags=["tasks"])
async def delete_task(task_id: int) -> Response:
	async with SessionLocal() as session:
		task = (await session.execute(select(Task).where(Task.id == task_id))).scalar_one_or_none()
		if task is None:
			raise HTTPException(status_code=404, detail="Task not found")
		await session.delete(task)
		await session.commit()
		return Response(status_code=status.HTTP_204_NO_CONTENT)
