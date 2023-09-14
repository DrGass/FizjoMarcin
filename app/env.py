from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Env(BaseSettings):
    port: int = 8000
    host: str = "0.0.0.0"
    environment: str = "development"

    postgres_user: str
    postgres_password: str 
    postgres_database: str 
    postgres_host: str 
    postgres_port: int 
    postgres_image_tag: str 
    
    # PORT=8000

    # POSTGRES_USER=user
    # POSTGRES_DATABASE=FizjoMarcin
    # POSTGRES_PASSWORD=password123
    # POSTGRES_HOST=postgres_database
    # POSTGRES_PORT=5432
    # POSTGRES_IMAGE_TAG=16rc1

    class Settings(BaseSettings):
        model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

@lru_cache
def get_env():
    return Env()
