from functools import lru_cache
from typing import List

from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    app_name: str = "No-Code ML Pipeline Builder"
    cors_origins: List[AnyHttpUrl] = []

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
