from sqlalchemy import Column, Enum, String, BINARY
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from src.db.postgres import Base
from typing import Union


class UserOrm(Base):
    __tablename__ = "users"

    id: UUID = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False
    )
    avatar: bytes = Column(BINARY())  # путь к аватарке
    sex: bytes = Column(Enum("man", "woman", name="sex"))  # пол
    first_name: str = Column(String())
    last_name: str = Column(String())
    email: str = Column(String(), unique=True, nullable=False)
    password: str = Column(String(), nullable=False)


MODELS = Union[UserOrm]
