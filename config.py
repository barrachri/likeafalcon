import logging
import os

log = logging.getLogger(__name__)


class Config():
    """General config class."""

    # Base folder
    BASE = os.path.dirname(__file__)

    # STREAM
    STREAM_URI = os.getenv("STREAM_URI", "nats://127.0.0.1:4222")

    # DATABASE_URI
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "mysecretpassword")
    DB_NAME = os.getenv("DB_NAME", "likeafalcon")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", 5432)

    # LOGGING CONFIGURATION
    DEFAULT_LOGGING = {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(levelname)s][%(filename)s:%(lineno)d]: %(asctime)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },
        "handlers": {
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout"
            },
        },
        "loggers": {
            "": {
                "level": "DEBUG",
                "handlers": ["console"],
                'propagate': False
            },
            "aiohttp.access": {
                "level": "DEBUG",
                "handlers": ["console"],
                'propagate': False
            }
        },
        "disable_existing_loggers": False
    }
