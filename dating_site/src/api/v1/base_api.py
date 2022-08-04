from typing import Optional
from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from http import HTTPStatus

from src.service.service import DBService, get_service
from src.models.user_model import MODELS
from src.settings import settings
from asyncio import wait_for, TimeoutError


class BaseAPI:
    service: Optional[DBService] = Depends(get_service)

    async def set_data(self, obj: MODELS):
        try:
            await wait_for(self.service.set_data(obj), timeout=settings.db.timeout)
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
            await wait_for(self.service.get_data(obj), timeout=settings.db.timeout)
        except ConnectionRefusedError:
            message = "The service is temporarily unavailable, try again later"
            print("e")
            raise HTTPException(
                status_code=HTTPStatus.SERVICE_UNAVAILABLE, detail=message
            )


def get_error_message(error: IntegrityError) -> dict[str, str]:
    """Разбирает сообщение об ошибке и возвращает словарик с полями которые не являются уникальными"""
    res = error.args[0].split("DETAIL:")
    lst = res[1].split('"')[1].split("=")
    err_msg = {lst[0][1:-1]: f"{lst[1][1:-1]} busy, change the field name"}
    return err_msg
