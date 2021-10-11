import logging
import os

try:
    from settings import local
except ImportError:
    logging.info("Local settings is missing")
    local = None


if local:
    DATABASE = local.DATABASE
else:
    DATABASE = {
        "user": os.getenv("DATABASE_USER", None),
        "password": os.getenv("DATABASE_PASSWORD", None),
        "address": os.getenv("DATABASE_ADDRESS", None),
        "name": os.getenv("DATABASE_NAME", None),
    }
