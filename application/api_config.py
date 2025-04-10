from pydantic_settings import BaseSettings, SettingsConfigDict


class Configs(BaseSettings):
    """Base class for all configurations."""

    SECRET: str = ""
    ACCESS_TIME: int = 432000
    REFRESH_TIME: int = 864000
    DEFAULT_SIZE: int = 10
    MIN_SIZE: int = 5
    MAX_SIZE: int = 50
    ACCESS_TOKEN_TAG: str = "Authorization"
    REFRESH_TOKEN_TAG: str = "Refresher"
    ACCESS_TOKEN_LENGTH: int = 72
    REFRESH_TOKEN_LENGTH: int = 128,
    SET_ALEMBIC: int = 0
    PATH: str = "app:app"
    HOST: str = "0.0.0.0"
    PORT: str = "8888"
    LOG_LEVEL: str = "info"
    RELOAD: int = 1

    model_config = SettingsConfigDict(env_file="../api.env", env_prefix="API_")


api_configs = Configs()
print('api_configs', api_configs)
