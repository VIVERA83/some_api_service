import os
from pydantic import BaseSettings
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))
load_dotenv()


class PostgresSettings(BaseSettings):
    pg_schema: str
    pg_user: str
    pg_password: str
    pg_host: str
    pg_port: int
    pg_db_name: str

    @property
    def pg_dsn(self):
        return f"{self.pg_schema}://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_db_name}"


class Settings:
    db = PostgresSettings()


settings = Settings()
