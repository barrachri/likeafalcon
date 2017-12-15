"""
Module imported by the models
Used to avoid circular imports.
"""

from sqlalchemy import MetaData

metadata = MetaData()
