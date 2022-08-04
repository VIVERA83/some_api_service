from pydantic import BaseSettings
from dotenv import load_dotenv

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
