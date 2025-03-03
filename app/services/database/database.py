from contextlib import contextmanager
from functools import lru_cache
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session, Session


DATABASE_URL = ""

# Configure the database engine with proper pooling
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connection before using
    pool_size=20,  # Maximum number of permanent connections
    max_overflow=10,  # Maximum number of additional connections
    pool_recycle=3600,  # Recycle connections after 1 hour
    pool_timeout=30,  # Wait up to 30 seconds for a connection
    echo=False,  # Set to True for debugging SQL queries
)

Base = declarative_base()


# Create a cached session factory
@lru_cache()
def get_session_factory() -> scoped_session:
    """Create a thread-safe session factory."""
    session_local = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,  # Prevent expired object issues
    )
    return scoped_session(session_local)


# Get database session with proper connection management
@contextmanager
def get_db() -> Generator[Session, None, None]:
    """Get database session with proper connection management.

    This context manager ensures:
    - Proper connection pooling
    - Session cleanup
    - Connection return to pool
    - Thread safety

    Yields:
        Session: SQLAlchemy session object
    """
    session_factory = get_session_factory()
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
        session_factory.remove()  # Clean up the session from the registry
