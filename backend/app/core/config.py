from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    DATABASE_URL: str = "postgresql+asyncpg://shakar:shakar@localhost:5432/shakar_db"
    SECRET_KEY: str = "change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    PROJECT_NAME: str = "فروشگاه شاکار"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: list[str] = Field(default_factory=list)
    FIRST_SUPERUSER_EMAIL: str = "admin@shakar.ir"
    FIRST_SUPERUSER_PASSWORD: str = "Admin@123456"

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: Any) -> list[str]:
        if value is None or value == "":
            return []
        if isinstance(value, list):
            return [str(item).strip() for item in value]
        if isinstance(value, str):
            raw = value.strip()
            if raw.startswith("["):
                return [str(item).strip() for item in json.loads(raw)]
            return [item.strip() for item in raw.split(",") if item.strip()]
        raise ValueError("Invalid BACKEND_CORS_ORIGINS value")


@lru_cache
def get_settings() -> Settings:
    return Settings()
