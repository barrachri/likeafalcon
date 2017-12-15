"""Creating tables."""

from sqlalchemy import create_engine

from app import models  # noqa:F401
from config import Config as C
from factory import metadata


def create_tables():
    """Create db tables."""
    dsn = f"postgresql+psycopg2://{C.DB_USER}:{C.DB_PASSWORD}@{C.DB_HOST}/{C.DB_NAME}"
    try:
        engine = create_engine(dsn)
        metadata.create_all(engine)
        print("Tables created")
    except Exception:
        print("Something went wrong!")
        raise


if __name__ == "__main__":
    create_tables()
