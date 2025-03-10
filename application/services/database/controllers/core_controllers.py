from typing import Type, TypeVar

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from fastapi import status
from fastapi.exceptions import HTTPException

from application.services.database.database import get_db


# Type variable for class methods returning self
T = TypeVar("T", bound="FilterAttributes")


class BaseAlchemyModel:
    """
    Controller of alchemy to database transactions.
    Query: Query object for model
    Session: Session object for model
    Actions: save, flush, rollback, commit
    """

    __abstract__ = True

    @classmethod
    def new_session(cls) -> Session:
        """Get database session."""

        with get_db() as session:
            return session

    @classmethod
    def flush(cls: Type[T], db: Session) -> T:
        """
        Flush the current session to the database.

        Args:
            db: Database session

        Returns:
            Self instance

        Raises:
            HTTPException: If database operation fails
        """
        try:
            db.flush()
            return cls
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail={
                    "message": "Database operation failed",
                },
            )

    def destroy(self: Type[T], db: Session) -> None:
        """
        Delete the record from the database.

        Args:
            db: Database session
        """
        db.delete(self)

    @classmethod
    def save(cls: Type[T], db: Session) -> None:
        """
        Commit changes to database.

        Args:
            db: Database session

        Raises:
            HTTPException: If commit fails
        """
        try:
            db.commit()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail={
                    "message": "Alchemy save operation failed",
                    "error": str(e),
                },
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "message": "Unknown exception raised.",
                    "error": str(e),
                },
            )

    @classmethod
    def rollback(cls: Type[T], db: Session) -> None:
        """
        Rollback current transaction.

        Args:
            db: Database session
        """
        db.rollback()
