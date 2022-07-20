from pydantic import BaseModel, EmailStr, UUID4, validator
from enum import Enum
import json


class Sex(str, Enum):
    man = "man"
    women = "women"


class UserModel(BaseModel):
    _id: UUID4 = None
    avatar: str = "avatar"
    sex: Sex
    first_name: str = None
    last_name: str = None
    email: EmailStr
    password: str

    @validator("password")
    def check_password(cls, v: str):  # noqa
        if len(v) < 6:
            raise ValueError("The password must be at least 6 characters long")
        return v
