import os
from pydantic import BaseSettings
from dotenv import load_dotenv

# "/../.env_local"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))
load_dotenv(".env_local")


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
