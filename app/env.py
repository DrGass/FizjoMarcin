from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Env(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )

    port: int = 8000
    host: str = "0.0.0.0"
    environment: str
    postgres_user: str
    postgres_password: str
    postgres_database: str
    postgres_host: str
    postgres_port: int
    postgres_image_tag: str

    # postgres_user: str="user"
    # postgres_password: str  ="FizjoMarcin"
    # postgres_database: str ="password123"
    # postgres_host: str ="postgres_database"
    # postgres_port: int =5432
    # postgres_image_tag: str  ="15-alpine3.17"


@lru_cache
def get_env():
    return Env()
