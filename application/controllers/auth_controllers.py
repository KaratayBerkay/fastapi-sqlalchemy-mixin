import secrets
import hashlib

from application.api_config import Configs


class PasswordModule:

    @staticmethod
    def generate_token(length=32):
        return secrets.token_urlsafe(length)

    @staticmethod
    def create_hashed_password(salt: str, id_: str, password: str):
        return hashlib.sha256(f"{salt}:{id_}:{password}".encode("utf-8")).hexdigest()

    @classmethod
    def check_password(cls, salt: str, id_: str, password: str, password_hashed: str):
        return cls.create_hashed_password(salt, id_, password) == password_hashed

    @classmethod
    def generate_access_token(cls):
        return cls.generate_token(Configs.ACCESS_TOKEN_LENGTH)

    @classmethod
    def generate_refresh_token(cls):
        return cls.generate_token(Configs.REFRESH_TOKEN_LENGTH)
