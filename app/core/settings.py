# app/core/settings.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = "local"

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    # Local-only
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None

    DEBUG: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
