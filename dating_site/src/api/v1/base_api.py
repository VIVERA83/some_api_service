from typing import Optional
from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from http import HTTPStatus

from src.service.service import Service, get_service
from src.models.user_model import MODELS


class BaseAPI:
    service: Optional[Service] = Depends(get_service)

    async def set_data(self, obj: MODELS):
        try:
            await self.service.set_data(obj)
        except IntegrityError as e:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=get_error_message(e))


def get_error_message(error: IntegrityError):
    res = error.args[0].split("DETAIL:")
    lst = res[1].split('"')[1].split("=")
    err_msg = {lst[0][1:-1]: f"{lst[1][1:-1]} busy, change the field name"}
    return err_msg
