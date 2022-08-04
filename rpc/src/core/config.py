import os
from pydantic import BaseSettings
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))
load_dotenv()


class RabbitSettings(BaseSettings):
    rabbit_dsn: str


class YandexDiskSettings(BaseSettings):
    ya_secret: str
    ya_token: str


class Settings:
    rabbit = RabbitSettings()
    ya = YandexDiskSettings()


settings = Settings()
