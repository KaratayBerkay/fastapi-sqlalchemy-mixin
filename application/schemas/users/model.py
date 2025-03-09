from sqlalchemy import String
from sqlalchemy.orm import mapped_column

from services.database.controllers.mixin_controllers import CrudMixin


class User(CrudMixin):

    __tablename__ = "users"

    email: str = mapped_column(String, unique=True, nullable=False, index=True)
    name: str = mapped_column(String, nullable=False)
    surname: str = mapped_column(String, nullable=False)
    hashed_password: str = mapped_column(String, nullable=False)
