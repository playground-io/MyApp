"""SQLAlchemy persistence models.

This file defines the shape of the tables in the database. Each class here maps
straight to a database table.
"""

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Task(Base):
    """A task that can be completed or removed.

    The `Task` model matches a table named `tasks` in SQLite. Every field below
    is a column in that table.
    """

    __tablename__ = "tasks"

    # `id` is the unique identifier for each task.
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # `title` must exist and has a max length of 200 characters.
    title: Mapped[str] = mapped_column(String(200), nullable=False)

    # `description` is optional, so it can be null in the database.
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # `completed` starts as false unless the app sets it to true.
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # `created_at` stores the exact time when the task was created.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
