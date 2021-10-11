from pydantic import BaseSettings

from settings.base import DATABASE


class DatabaseSettings(BaseSettings):
    user: str
    password: str
    address: str
    name: str


DB_SETTINGS = DatabaseSettings(**DATABASE)
