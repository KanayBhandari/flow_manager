# app/db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import config

_engine = None
_SessionLocal = None

def _init_engine():
    global _engine, _SessionLocal

    if _engine is None:
        _engine = create_engine(
            config.DATABASE_URL,
            pool_size=2,          # Lambda-safe
            max_overflow=0,       # IMPORTANT
            pool_pre_ping=True
        )
        _SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=_engine
        )

def get_db():
    _init_engine()
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()
