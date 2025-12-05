# app/core/config.py

from app.core.settings import settings

class Config:
    @property
    def DATABASE_URL(self):
        return (
            f"postgresql+psycopg2://{settings.POSTGRES_USER}:"
            f"{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:"
            f"{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
        )

config = Config()
