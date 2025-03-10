from sqlalchemy import (
    Text,
    String,
    UUID,
    ForeignKey,
)
from sqlalchemy.orm import mapped_column, relationship, Mapped
from application.services.database.controllers.mixin_controllers import CrudMixin


class Notes(CrudMixin):

    __tablename__ = "notes"

    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    user_uu_id: Mapped[str] = mapped_column(
        UUID, ForeignKey("users.uu_id"), nullable=False
    )

    comments = relationship("Comments", back_populates="notes")
    tags = relationship("Tags", back_populates="notes")


class Comments(CrudMixin):

    __tablename__ = "comments"

    content: Mapped[str] = mapped_column(Text, nullable=False)
    note_uu_id: Mapped[str] = mapped_column(
        UUID, ForeignKey("notes.uu_id"), nullable=False
    )
    user_uu_id: Mapped[str] = mapped_column(
        UUID, ForeignKey("users.uu_id"), nullable=False
    )

    notes = relationship("Notes", back_populates="comments")


class Tags(CrudMixin):

    __tablename__ = "tags"

    name: Mapped[str] = mapped_column(String, nullable=False)
    note_uu_id: Mapped[str] = mapped_column(
        UUID, ForeignKey("notes.uu_id"), nullable=False
    )
    user_uu_id: Mapped[str] = mapped_column(
        UUID, ForeignKey("users.uu_id"), nullable=False
    )

    notes = relationship("Notes", back_populates="tags")
