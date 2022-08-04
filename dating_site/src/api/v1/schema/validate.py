from enum import Enum
from fastapi import UploadFile, HTTPException
from http import HTTPStatus


class TypeFile(str, Enum):
    jpeg = "jpeg"
    png = "png"


async def validate_file(file: UploadFile):
    # проверка на тип пересылаемого файла
    type_file = file.content_type.split("/")[1]
    try:
        TypeFile(type_file)
    except ValueError:
        raise HTTPException(
            status_code=HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
            detail={type_file: "is not a valid file type"},
        )
    if len(await file.read()) >= 1048576:
        raise HTTPException(
            status_code=HTTPStatus.REQUEST_ENTITY_TOO_LARGE, detail="Too large"
        )
