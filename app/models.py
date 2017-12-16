"""App models."""

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Integer,
    Table,
)
from sqlalchemy.sql import func

from factory import metadata

Event = Table(
    'events',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('created_at', DateTime(timezone=True),
           server_default=func.now()),
    Column('data', JSON),
)
