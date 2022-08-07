import io
from typing import Optional
from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from http import HTTPStatus

from src.service.db_service import DBService, get_db_service
from src.service.rpc_service import RPCService, get_rpc_service
from src.models.user_model import MODELS
from src.settings import settings
from asyncio import wait_for, TimeoutError


class BaseAPI:
    db_service: Optional[DBService] = Depends(get_db_service)
    rpc_service: Optional[RPCService] = Depends(get_rpc_service)

    async def set_data(self, obj: MODELS):
        try:
            await wait_for(self.db_service.set_data(obj), timeout=settings.db.timeout)
        except IntegrityError as e:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail=get_error_message(e)
            )
        except TimeoutError as e:
            message = "The service is temporarily unavailable, try again later"
            raise HTTPException(
                status_code=HTTPStatus.SERVICE_UNAVAILABLE, detail=message
            )
        except ConnectionRefusedError:
            message = "The service is temporarily unavailable, try again later"
            raise HTTPException(
                status_code=HTTPStatus.SERVICE_UNAVAILABLE, detail=message
            )

    async def get_data(self, obj: MODELS):
        try:
            await wait_for(self.db_service.get_data(obj), timeout=settings.db.timeout)
        except ConnectionRefusedError:
            message = "The service is temporarily unavailable, try again later"
            raise HTTPException(
                status_code=HTTPStatus.SERVICE_UNAVAILABLE, detail=message
            )

    async def upload_image(self, fd: bytes, file_name: str):
        """
        Загрузка изображения в Yandex Disk, предварительно на изображение наносится текст
        :param fd: Изображение, в виде байтового объекта.
        :param file_name: Имя файла.
        :return:
        """
        print("upload_image", file_name)
        return await self.rpc_service.call(
            receiver=settings.rpc.receiver_queue,
            method_name="upload_image",
            kwargs={"fd": fd, "file_name": file_name, "text": "Проруха судьба"},
        )


def get_error_message(error: IntegrityError) -> dict[str, str]:
    """Разбирает сообщение об ошибке и возвращает словарик с полями которые не являются уникальными"""
    if isinstance(error, IntegrityError):
        res = error.args[0].split("DETAIL:")
        key = res[1].split("=")[0].split(" ")[-1][1:-1]
        value = res[1].split("=")[1].split(" ")[0][1:-1]
        err_msg = {key: f"{value} busy, change the field name"}
    else:
        err_msg = {"error": str(error)}
    return err_msg
