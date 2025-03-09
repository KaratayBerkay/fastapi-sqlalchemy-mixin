from pydantic_settings import BaseSettings, SettingsConfigDict


class Configs(BaseSettings):
    """Base class for all configurations."""

    SECRET: str = ""
    ACCESS_TIME: int = 432000
    REFRESH_TIME: int = 864000

    model_config = SettingsConfigDict(env_file="/api.env", env_prefix="API_")

api_configs = Configs()
