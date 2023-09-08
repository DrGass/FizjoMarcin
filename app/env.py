from pydantic_settings import BaseSettings
from functools import lru_cache


class Env(BaseSettings):
    port: int = 8000
    host: str = "0.0.0.0"

    postgres_user: str = "user"
    postgres_password: str = "password123"
    postgres_database: str = "FizjoMarcin"
    postgres_host: str = ""
    postgres_port: int = "5432"
    
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

@lru_cache
def get_env():
    return Env()
