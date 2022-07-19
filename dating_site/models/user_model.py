from sqlalchemy import Column, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from db.postgres import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    avatar = Column(String())  # путь к аватарке
    sex = Column(Enum("man", "woman", name="sex"))  # пол
    first_name = Column(String())
    last_name = Column(String())

    email = Column(String(), unique=True, nullable=False)
    password = Column(String(), nullable=False)
