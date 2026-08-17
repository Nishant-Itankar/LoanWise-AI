from sqlalchemy import create_engine

from src.config import (
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_NAME,
    DATABASE_USER,
    DATABASE_PASSWORD,
)


def get_database_url() -> str:
    return (
        f"postgresql+psycopg2://"
        f"{DATABASE_USER}:{DATABASE_PASSWORD}"
        f"@{DATABASE_HOST}:{DATABASE_PORT}"
        f"/{DATABASE_NAME}"
    )


def get_engine():
    return create_engine(
        get_database_url(),
        pool_pre_ping=True,
    )