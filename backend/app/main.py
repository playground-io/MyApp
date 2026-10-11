"""FastAPI application and task endpoints.

This is the main API file. It defines the HTTP routes, handles validation, and
connects the frontend to the database.
"""

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
    """Create missing tables when the API starts.

    The app runs this once during startup. It ensures the SQLite tables exist
    before any route tries to use them.
    """
    Base.metadata.create_all(bind=engine)
    yield


# Create the FastAPI app instance.
# The app object is what receives HTTP requests and routes them to the correct
# function below.
app = FastAPI(
    title="MyApp API",
    description="Task-tracker API for the MyApp starter.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS lets the frontend running on localhost:3000 talk to the backend.
# This is important because browsers block requests from different origins by
# default unless we explicitly allow them.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This alias makes the database session easy to use in every route.
# FastAPI will inject the session using the `get_db` dependency.
DatabaseSession = Annotated[Session, Depends(get_db)]


@app.get("/health")
def health_check() -> dict[str, str]:
    """Report that the API process is responsive.

    A quick check for monitoring or debugging. It simply tells us the server is
    alive.
    """
    return {"status": "ok"}


@app.get("/api/tasks", response_model=list[TaskRead])
def list_tasks(
    db: DatabaseSession,
    completed: Annotated[bool | None, Query()] = None,
) -> list[Task]:
    """Return tasks, optionally filtered by completion state.

    `select(Task)` tells SQLAlchemy: "give me every task row in the tasks table".
    We sort the newest tasks first so the UI shows the latest items first.
    """
    statement = select(Task).order_by(Task.created_at.desc(), Task.id.desc())
    if completed is not None:
        # If the client passes ?completed=true or false, filter by that value.
        statement = statement.where(Task.completed == completed)
    return list(db.scalars(statement).all())


@app.post(
    "/api/tasks",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
)
def create_task(payload: TaskCreate, db: DatabaseSession) -> Task:
    """Validate and persist a new task.

    The payload is validated by the `TaskCreate` schema before this function runs.
    If validation passes, we create a `Task` object and save it to the database.
    """
    task = Task(title=payload.title, description=payload.description)
    db.add(task)  # Add the new object to the current SQLAlchemy session.
    db.commit()  # Save it to the database.
    db.refresh(task)  # Load the generated database fields (like id and created_at).
    return task


@app.patch("/api/tasks/{task_id}", response_model=TaskRead)
def update_task(task_id: int, payload: TaskUpdate, db: DatabaseSession) -> Task:
    """Update a task's completion state.

    The client sends the id of the task and a new `completed` value.
    """
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
    """Delete a task or return 404 when it does not exist.

    A 204 response means "no content". This is a common HTTP status for a
    successful delete.
    """
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    db.delete(task)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
