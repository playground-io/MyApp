"""Validated API request and response models."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    """Fields accepted when creating a task."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)


class TaskUpdate(BaseModel):
    """Fields accepted when updating a task."""

    model_config = ConfigDict(extra="forbid")

    completed: bool


class TaskRead(BaseModel):
    """Task representation returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime
