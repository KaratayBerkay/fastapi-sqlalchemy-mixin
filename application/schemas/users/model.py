from application.services.database.controllers.mixin_controllers import CrudMixin

from sqlalchemy import String, Text, UUID
from sqlalchemy.orm import mapped_column, Mapped, relationship


class User(CrudMixin):

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False)
    user_uu_id: Mapped[str] = mapped_column(UUID, nullable=False)

    tokens = relationship("Token", back_populates="user")
