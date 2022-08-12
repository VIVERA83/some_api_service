from sqlalchemy import Column, Enum, String, BINARY, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from typing import Union
from src.service.db.postgres import Base


class User(Base):
    __tablename__ = "users"

    id: UUID = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False
    )
    sex = Column(Enum("man", "woman", name="sex"))  # пол
    first_name = Column(String())
    last_name = Column(String())
    email = Column(String(), unique=True, nullable=False)
    password = Column(String(), nullable=False)

    avatars = relationship("Avatar", lazy="joined", cascade="all,delete", uselist=True)
    geodata = relationship("Geodata", lazy="joined", cascade="all,delete", uselist=True)


class Avatar(Base):
    __tablename__ = "avatars"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    avatar = Column(String(), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))


class GeoData(Base):
    __tablename__ = "geodata"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    geodata = Column(String(), nullable=False)
    city = Column(String(), nullable=False)
    latitude = Column(String(), nullable=False)
    longitude = Column(String(), nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))


MODELS = Union[User, Avatar]
