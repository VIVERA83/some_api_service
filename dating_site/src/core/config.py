import os
from pydantic import BaseSettings
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))
# "../.env_local"
load_dotenv("../.env_local")


class PostgresSettings(BaseSettings):
    postgres_schema: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db_name: str
    timeout: int

    @property
    def pg_dsn(self):
        return f"{self.postgres_schema}://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db_name}"


class AppSettings(BaseSettings):
    app_name: str
    docs_url: str
    openapi_url: str
    description: str
    version: str


class RPCSettings(BaseSettings):
    rabbit_dsn: str
    listen_queue: str
    receiver_queue: str
    image_service: str
    geo_service: str


class Settings:
    # время, которое ждем ответа от БД
    timeout: int

    db = PostgresSettings()
    app = AppSettings()
    rpc = RPCSettings()


settings = Settings()
