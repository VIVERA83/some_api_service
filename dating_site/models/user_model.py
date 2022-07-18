from uuid import uuid4

from sqlalchemy import String, Enum
from sqlalchemy.dialects.postgresql import UUID

from db.postgres import db_postgres


class Sex(Enum):
    man = 0
    woman = 1


class User(db_postgres.Model):
    __tablename__ = "users"

    id = db_postgres.Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    avatar = db_postgres.Column(String())  # путь к аватарке
    sex = db_postgres.Column(Enum(Sex))  # пол
    first_name = db_postgres.Column(String())
    last_name = db_postgres.Column(String())

    email = db_postgres.Column(String(), unique=True, nullable=False)
    password = db_postgres.Column(String(), nullable=False)
