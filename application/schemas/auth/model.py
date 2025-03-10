from application.services.database.controllers.mixin_controllers import CrudMixin

from sqlalchemy import ForeignKey, String, UUID
from sqlalchemy.orm import mapped_column, relationship, Mapped


class Token(CrudMixin):

    __tablename__ = "tokens"

    token: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    user_uu_id: Mapped[str] = mapped_column(
        UUID, ForeignKey("users.uu_id"), nullable=False
    )

    user = relationship("User", back_populates="tokens")
