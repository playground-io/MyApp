"""Validated API request and response models.

Pydantic schemas act like a contract for the API. They check incoming data and
shape the data returned to the frontend.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    """Fields accepted when creating a task.

    This is used for a POST request like /api/tasks. The app validates that the
    title is not empty and the description is not too long.
    """

    # Reject unknown keys and trim whitespace from text input.
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    # Title is required and must be between 1 and 200 characters.
    title: str = Field(min_length=1, max_length=200)

    # Description is optional, but if present it cannot exceed 2000 chars.
    description: str | None = Field(default=None, max_length=2000)


class TaskUpdate(BaseModel):
    """Fields accepted when updating a task.

    For a PATCH request, the client sends only the fields it wants to change.
    """

    # Prevent extra/unexpected properties from being sent.
    model_config = ConfigDict(extra="forbid")

    # The task completion status is a boolean: true = done, false = not done.
    completed: bool


class TaskRead(BaseModel):
    """Task representation returned by the API.

    FastAPI can convert a SQLAlchemy model object into this schema because of
    `from_attributes=True`.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime
