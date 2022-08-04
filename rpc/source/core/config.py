from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class RabbitSettings(BaseSettings):
    rabbit_dsn: str


class YandexDiskSettings(BaseSettings):
    ya_secret: str
    ya_token: str


class RPCSettings(BaseSettings):
    queue_name: str


class Settings:
    rabbit = RabbitSettings()
    ya = YandexDiskSettings()
    rpc = RPCSettings()


settings = Settings()
