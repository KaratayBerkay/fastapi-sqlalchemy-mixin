from pydantic_settings import BaseSettings, SettingsConfigDict


class Configs(BaseSettings):
    """Base class for all configurations."""

    DB: str = ""
    USER: str = ""
    PASSWORD: str = ""
    HOST: str = ""
    PORT: int = 5432
    ENGINE: str = ""

    @property
    def url(self):
        return f"{self.ENGINE}://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}"

    model_config = SettingsConfigDict(env_file="postgres.env", env_prefix="POSTGRES_")


postgres_configs = Configs()
