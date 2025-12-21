# app/core/config.py

from app.core.settings import settings
from app.core.secrets_manager_app import get_db_credentials

class Config:
    @property
    def DATABASE_URL(self):
        if settings.ENV == "local":
            username = settings.POSTGRES_USER
            password = settings.POSTGRES_PASSWORD
        else:
            username, password = get_db_credentials()

        return (
            f"postgresql+psycopg2://{username}:"
            f"{password}@{settings.POSTGRES_HOST}:"
            f"{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
        )

config = Config()
