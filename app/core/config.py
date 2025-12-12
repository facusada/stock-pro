from __future__ import annotations

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_name: str = "Stock Backend"
    secret_key: str = "CHANGE_ME"
    access_token_expire_minutes: int = 60
    algorithm: str = "HS256"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/stock_db"
    environment: str = "development"
    api_prefix: str = "/api"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
