import arrow
import datetime

from typing import Optional, Any, Dict
from sqlalchemy.orm import Session, Mapped
from pydantic import BaseModel
from fastapi.exceptions import HTTPException

from decimal import Decimal
from sqlalchemy import TIMESTAMP, NUMERIC
from sqlalchemy.orm.attributes import InstrumentedAttribute

# from application.services.database.controllers.core_controllers import BaseAlchemyModel


class Credentials(BaseModel):
    person_id: int
    person_name: str
    full_name: Optional[str] = None


class MetaData:
    """
    Class to store metadata for a query.
    """
    created: bool = False
    updated: bool = False


class CRUDModel:

    __abstract__ = True

    creds: Credentials = None
    meta_data: MetaData = MetaData()

    @classmethod
    def create_credentials(cls, record_created) -> None:
        """
        Save user credentials for tracking.

        Args:
            record_created: Record that created or updated
        """
        if getattr(cls.creds, "person_id", None) and getattr(cls.creds, "person_name", None):
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
    def iterate_over_variables(cls, val: Any, key: str) -> tuple[bool, Optional[Any]]:
        """
        Process a field value based on its type and convert it to the appropriate format.

        Args:
            val: Field value
            key: Field name

        Returns:
            Tuple of (should_include, processed_value)
        """
        key_ = cls.__annotations__.get(key, None)
        is_primary = key in cls.primary_keys
        row_attr = bool(getattr(getattr(cls, key), "foreign_keys", None))

        # Skip primary keys and foreign keys
        if is_primary or row_attr:
            return False, None

        if val is None:  # Handle None values
            return True, None

        if str(key[-5:]).lower() == "uu_id":  # Special handling for UUID fields
            return True, str(val)

        if key_:        # Handle typed fields
            if key_ == Mapped[int]:
                return True, int(val)
            elif key_ == Mapped[bool]:
                return True, bool(val)
            elif key_ == Mapped[float] or key_ == Mapped[NUMERIC]:
                return True, round(float(val), 3)
            elif key_ == Mapped[TIMESTAMP]:
                return True, str(arrow.get(str(val)).format("YYYY-MM-DD HH:mm:ss ZZ"))
            elif key_ == Mapped[str]:
                return True, str(val)
        else:           # Handle based on Python types
            if isinstance(val, datetime.datetime):
                return True, str(arrow.get(str(val)).format("YYYY-MM-DD HH:mm:ss ZZ"))
            elif isinstance(val, bool):
                return True, bool(val)
            elif isinstance(val, (float, Decimal)):
                return True, round(float(val), 3)
            elif isinstance(val, int):
                return True, int(val)
            elif isinstance(val, str):
                return True, str(val)
            elif val is None:
                return True, None

        return False, None

    def get_dict(self, exclude_list: Optional[list[InstrumentedAttribute]] = None) -> Dict[str, Any]:
        """
        Convert model instance to dictionary with customizable fields.
        Returns:
            Dictionary representation of the model
            Dictionary returns only UUID fields and fields that are not in exclude_list
        """
        return_dict: Dict[str, Any] = {}    # Handle default field selection
        exclude_list = exclude_list or []
        exclude_list = [exclude_arg.key for exclude_arg in exclude_list]

        columns_set = set(self.columns)
        columns_list = set([col for col in list(columns_set) if str(col)[-2:] != "id"])
        columns_extend = set(col for col in list(columns_set) if str(col)[-5:].lower() == "uu_id")
        columns_list = set(columns_list) | set(columns_extend)
        columns_list = list(set(columns_list) - set(exclude_list))

        for key in columns_list:
            val = getattr(self, key)
            correct, value_of_database = self.iterate_over_variables(val, key)
            if correct:
                return_dict[key] = value_of_database

        return return_dict

    @classmethod
    def find_or_create(
            cls, db: Session, exclude_args: Optional[list[InstrumentedAttribute]] = None, **kwargs
    ):
        """
        Find an existing record matching the criteria or create a new one.

        Args:
            db: Database session
            exclude_args: Keys to exclude from search
            **kwargs: Search/creation criteria

        Returns:
            Existing or newly created record
        """
        # Search for existing record
        query = db.query(cls).filter(
            cls.expiry_ends > str(arrow.now()), cls.expiry_starts <= str(arrow.now()),
        )
        exclude_args = exclude_args or []
        exclude_args = [exclude_arg.key for exclude_arg in exclude_args]
        for key, value in kwargs.items():
            if hasattr(cls, key) and key not in exclude_args:
                query = query.filter(getattr(cls, key) == value)

        already_record = query.first()
        if already_record:  # Handle existing record
            cls.meta_data.created = False
            return already_record

        # Create new record
        created_record = cls()
        for key, value in kwargs.items():
            setattr(created_record, key, value)
        cls.create_credentials(created_record)

        db.add(created_record)
        db.flush()
        cls.meta_data.created = True
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
