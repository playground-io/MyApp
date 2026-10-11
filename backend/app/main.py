"""FastAPI application and task endpoints."""

import os
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Task
from app.schemas import TaskCreate, TaskRead, TaskUpdate


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Create missing tables when the API starts."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="MyApp API",
    description="Task-tracker API for the MyApp starter.",
    version="1.0.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DatabaseSession = Annotated[Session, Depends(get_db)]


@app.get("/health")
def health_check() -> dict[str, str]:
    """Report that the API process is responsive."""
    return {"status": "ok"}


@app.get("/api/tasks", response_model=list[TaskRead])
def list_tasks(
    db: DatabaseSession,
    completed: Annotated[bool | None, Query()] = None,
) -> list[Task]:
    """Return tasks, optionally filtered by completion state."""
    statement = select(Task).order_by(Task.created_at.desc(), Task.id.desc())
    if completed is not None:
        statement = statement.where(Task.completed == completed)
    return list(db.scalars(statement).all())


@app.post(
    "/api/tasks",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
)
def create_task(payload: TaskCreate, db: DatabaseSession) -> Task:
    """Validate and persist a new task."""
    task = Task(title=payload.title, description=payload.description)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@app.patch("/api/tasks/{task_id}", response_model=TaskRead)
def update_task(task_id: int, payload: TaskUpdate, db: DatabaseSession) -> Task:
    """Update a task's completion state."""
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    task.completed = payload.completed
    db.commit()
    db.refresh(task)
    return task


@app.delete("/api/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: DatabaseSession) -> Response:
    """Delete a task or return 404 when it does not exist."""
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    db.delete(task)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
