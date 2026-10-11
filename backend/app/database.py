"""SQLAlchemy engine and request-scoped database sessions.

This file is the connection between our Python app and the SQLite database.
For beginners: think of this as the bridge that opens a database connection
whenever a request needs to read or write data.
"""

import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# The database address can be changed with an environment variable.
# The default is a local SQLite file named app.db in the backend folder.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Create the SQLAlchemy engine.
# For SQLite, we need check_same_thread=False because a database connection may
# be shared across threads in a web app.
engine = create_engine(
    DATABASE_URL,
    connect_args=(
        {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
    ),
)

# A session factory creates a new database session each time we need one.
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models.

    All ORM models in this project inherit from Base, so SQLAlchemy knows how
    to map Python classes to database tables.
    """


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and close it when the request is complete.

    FastAPI calls this dependency for every endpoint. The `with` statement makes
    sure the session is always closed after the request ends.
    """
    with SessionLocal() as session:
        yield session
