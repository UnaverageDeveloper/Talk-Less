# Copyright (C) 2026 Talk-Less Contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# This file is part of Talk-Less.
#
# Talk-Less is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Talk-Less is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Talk-Less. If not, see <https://www.gnu.org/licenses/>.

"""
Database Connection and Session Management

This module provides database connection utilities.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from contextlib import contextmanager
import os
import logging

logger = logging.getLogger(__name__)

# Database URL from environment or default to SQLite for development
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'sqlite:///./talkless.db'  # Default to SQLite for easy development
)

# Create engine
# For SQLite, use StaticPool to allow multiple threads
if DATABASE_URL.startswith('sqlite'):
    engine = create_engine(
        DATABASE_URL,
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """
    Initialize database tables.
    Should be called once on application startup.
    """
    from .models import Base
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")


@contextmanager
def get_db_session() -> Session:
    """
    Get a database session as a context manager.
    
    Usage:
        with get_db_session() as session:
            # Use session
            pass
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db():
    """
    Dependency for FastAPI to get database sessions.
    
    Usage in FastAPI:
        @app.get("/endpoint")
        def endpoint(db: Session = Depends(get_db)):
            # Use db
            pass
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
