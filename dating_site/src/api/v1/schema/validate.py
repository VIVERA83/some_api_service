from enum import Enum
from fastapi import UploadFile, HTTPException, Request
from http import HTTPStatus


class TypeFile(str, Enum):
    jpeg = "jpeg"
    png = "png"


async def validate_file(file: UploadFile, request: Request):
    """
    Проверка файла на соответствие требованиям:
    1. тип файла: jpg, png
    2. размер файла не более 1 Мб.
    :param file: объект файл.
    :param request: запрос.
    :return:
    """
    max_size = 1024 * 1024 + 300  # на служебные данные
    if int(request.headers.get("content-length")) >= max_size:
        raise HTTPException(
            status_code=HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
            detail="Too large file to upload, maximum size 1MB",
        )

    type_file = file.content_type.split("/")[1]
    try:
        TypeFile(type_file)
    except ValueError:
        raise HTTPException(
            status_code=HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
            detail={type_file: "is not a valid file type"},
        )
