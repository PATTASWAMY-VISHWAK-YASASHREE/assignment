from functools import lru_cache
from typing import List

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "No-Code ML Pipeline Builder"
    cors_origins: List[AnyHttpUrl] = []
    API_KEY: str = "default-insecure-key"
    MAX_UPLOAD_SIZE_BYTES: int = 100 * 1024 * 1024  # 100 MB

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
