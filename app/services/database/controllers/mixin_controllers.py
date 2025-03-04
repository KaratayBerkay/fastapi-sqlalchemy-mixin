from sqlalchemy import (
    TIMESTAMP,
    NUMERIC,
    func,
    text,
    UUID,
    String,
    Integer,
    Boolean,
    SmallInteger,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_mixins.serialize import SerializeMixin
from sqlalchemy_mixins.repr import ReprMixin
from sqlalchemy_mixins.smartquery import SmartQueryMixin

from app.services.database.controllers.core_controllers import BaseAlchemyModel

from app.services.database.controllers.crud_controllers import CRUDModel
from app.services.database.controllers.filter_controllers import QueryModel
from app.services.database.database import Base


class BasicMixin(Base, BaseAlchemyModel):

    __abstract__ = True
    __repr__ = ReprMixin.__repr__


class CrudMixin(
    BasicMixin, CRUDModel, SerializeMixin, ReprMixin, SmartQueryMixin, QueryModel
):
    """
    Base mixin providing CRUD operations and common fields for PostgreSQL models.

    Features:
    - Automatic timestamps (created_at, updated_at)
    - Soft delete capability
    - User tracking (created_by, updated_by)
    - Data serialization
    - Multi-language support
    """

    __abstract__ = True

    # Primary and reference fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uu_id: Mapped[str] = mapped_column(
        UUID,
        server_default=text("gen_random_uuid()"),
        index=True,
        unique=True,
        comment="Unique identifier UUID",
    )

    # Common timestamp fields for all models
    expiry_starts: Mapped[TIMESTAMP] = mapped_column(
        type_=TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Record validity start timestamp",
    )
    expiry_ends: Mapped[TIMESTAMP] = mapped_column(
        type_=TIMESTAMP(timezone=True),
        default="2099-12-31",
        server_default="2099-12-31",
        comment="Record validity end timestamp",
    )


class BaseCollection(CrudMixin):
    """Base model class with minimal fields."""

    __abstract__ = True
    __repr__ = ReprMixin.__repr__


class CrudCollection(CrudMixin):
    """
    Full-featured model class with all common fields.

    Includes:
    - UUID and reference ID
    - Timestamps
    - User tracking
    - Confirmation status
    - Soft delete
    - Notification flags
    """

    __abstract__ = True
    __repr__ = ReprMixin.__repr__

    ref_id: Mapped[str] = mapped_column(
        String(100), nullable=True, index=True, comment="External reference ID"
    )

    # Timestamps
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
        comment="Record creation timestamp",
    )
    updated_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        index=True,
        comment="Last update timestamp",
    )

    created_by: Mapped[str] = mapped_column(
        String, nullable=True, comment="Creator name"
    )
    created_by_id: Mapped[int] = mapped_column(
        Integer, nullable=True, comment="Creator ID"
    )
    updated_by: Mapped[str] = mapped_column(
        String, nullable=True, comment="Last modifier name"
    )
    updated_by_id: Mapped[int] = mapped_column(
        Integer, nullable=True, comment="Last modifier ID"
    )

    # Status flags
    replication_id: Mapped[int] = mapped_column(
        SmallInteger, server_default="0", comment="Replication identifier"
    )
    deleted: Mapped[bool] = mapped_column(
        Boolean, server_default="0", comment="Soft delete flag"
    )
    active: Mapped[bool] = mapped_column(
        Boolean, server_default="1", comment="Record active status"
    )
