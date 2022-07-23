from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from fastapi import File, UploadFile, Request
from src.models.user_model import UserOrm
from src.api.v1.schema.user_schema import UserModel
from src.api.v1.base_api import BaseAPI
from src.api.v1.schema.validate import validate_file
from icecream import ic

import stun
import geocoder
import asyncio

client_router = InferringRouter()


def get_city_by_ip(ip: str = "199.7.157.0", count=1):
    # sec = random.randint(0, 3)
    # msg = f"count {count} sleep {sec} seconds"
    # yield ic(msg)
    result = geocoder.ip(ip)
    yield ic(count, result)
    ic(count)


@cbv(client_router)
class ClientApi(BaseAPI):

    @client_router.post("/create/", description="Зарегистрировать нового пользователя")
    async def create(self, request: Request, user: UserModel):
        """Create a new client"""
        ip = ic(request.client.host)
        ip = "199.7.157.0"
        # ic(await asyncio.get_running_loop().run_in_executor(None, lambda: geocoder.ip(ip)))
        # stun.get_ip_info()
        ic(await asyncio.get_running_loop().run_in_executor(None, lambda:  stun.get_ip_info()))
        # await self.set_data(UserOrm(**user.dict()))
        ic(request.headers.get("User-Agent"))
        return {"detail": "ok"}

    @client_router.post("/upload_avatar/", description="Загрузить аватар пользователя пользователя")
    async def upload_avatar(self, file: UploadFile | None = File()):
        await validate_file(file)
        return {"detail": "ok"}

    @client_router.get("/list/",
                       description="Посмотреть список пользователей")
    async def list(self):
        if users := await self.service.get_data(UserOrm):
            pass

        get_city_by_ip(count=1)

        return {"detail": users}
