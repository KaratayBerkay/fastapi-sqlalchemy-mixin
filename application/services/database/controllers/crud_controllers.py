import arrow

from typing import Optional, Any, Dict, List
from sqlalchemy.orm import Session, Mapped
from pydantic import BaseModel
from fastapi.exceptions import HTTPException

# from decimal import Decimal
# from sqlalchemy import TIMESTAMP, NUMERIC
# from application.services.database.controllers.core_controllers import BaseAlchemyModel


class Credentials(BaseModel):
    person_id: int
    person_name: str
    full_name: Optional[str] = None


class CRUDModel:

    __abstract__ = True

    creds: Credentials = None

    @classmethod
    def create_credentials(cls, record_created) -> None:
        """
        Save user credentials for tracking.

        Args:
            record_created: Record that created or updated
        """

        if getattr(cls.creds, "person_id", None) and getattr(
            cls.creds, "person_name", None
        ):
            record_created.created_by_id = cls.creds.person_id
            record_created.created_by = cls.creds.person_name
        return

    @classmethod
    def raise_exception(cls):
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Exception raised.",
            },
        )

    @classmethod
    def create_or_abort(cls, db: Session, **kwargs):
        """
        Create a new record or abort if it already exists.

        Args:
            db: Database session
            **kwargs: Record fields

        Returns:
            New record if successfully created
        """

        # Search for existing record
        query = db.query(cls).filter(
            cls.expiry_ends > str(arrow.now()),
            cls.expiry_starts <= str(arrow.now()),
        )

        for key, value in kwargs.items():
            if hasattr(cls, key):
                query = query.filter(getattr(cls, key) == value)

        already_record = query.first()
        # Handle existing record
        if already_record or already_record.deleted:
            cls.raise_exception()

        # Create new record
        created_record = cls()
        for key, value in kwargs.items():
            setattr(created_record, key, value)
        cls.create_credentials(created_record)
        db.add(created_record)
        db.flush()
        return created_record

    @classmethod
    def find_or_create(cls, db: Session, **kwargs):
        """
        Find an existing record matching the criteria or create a new one.

        Args:
            db: Database session
            **kwargs: Search/creation criteria

        Returns:
            Existing or newly created record
        """

        # Search for existing record
        query = db.query(cls).filter(
            cls.expiry_ends > str(arrow.now()),
            cls.expiry_starts <= str(arrow.now()),
        )

        for key, value in kwargs.items():
            if hasattr(cls, key):
                query = query.filter(getattr(cls, key) == value)

        already_record = query.first()
        if already_record:  # Handle existing record
            return already_record

        # Create new record
        created_record = cls()
        for key, value in kwargs.items():
            setattr(created_record, key, value)
        cls.create_credentials(created_record)
        db.add(created_record)
        db.flush()
        return created_record

    def update(self, db: Session, **kwargs):
        """
        Update the record with new values.

        Args:
            db: Database session
            **kwargs: Fields to update

        Returns:
            Updated record

        Raises:
            ValueError: If attempting to update is_confirmed with other fields
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.update_credentials()
        db.flush()
        return self

    def update_credentials(self) -> None:
        """
        Save user credentials for tracking.
        """
        # Update confirmation or modification tracking
        person_id = getattr(self.creds, "person_id", None)
        person_name = getattr(self.creds, "person_name", None)
        if person_id and person_name:
            self.updated_by_id = self.creds.person_id
            self.updated_by = self.creds.person_name
        return
