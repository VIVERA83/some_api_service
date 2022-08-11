import asyncio

from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from fastapi import File, UploadFile, Request
from src.models.user_model import UserOrm, Avatar
from src.api.v1.schema.user_schema import UserModel
from src.api.v1.base_api import BaseAPI
from src.api.v1.schema.validate import validate_file
from .utils import create_new_filename
from uuid import UUID
from icecream import ic

ic.includeContext = True
client_router = InferringRouter()


@cbv(client_router)
class ClientApi(BaseAPI):
    @client_router.post("/create/", description="Зарегистрировать нового пользователя")
    async def create(self, request: Request, user: UserModel):
        """Create a new client"""
        await self.set_data(UserOrm(**user.dict()))
        return {"detail": "ok"}

    @client_router.post("/upload_avatar/", description="Загрузить аватар пользователя")
    async def upload_avatar(self, request: Request, user_id: UUID, file: UploadFile | None = File()):
        await validate_file(file, request)
        result = "OK"
        try:
            link = await asyncio.wait_for(
                self.upload_image(fd=await file.read(),
                                  file_name=create_new_filename(user_id.hex, file.filename)),
                timeout=10)
            await self.set_data(Avatar(id=user_id, avatar=link))
        except asyncio.TimeoutError:
            result = "TimeoutError"
        return {"detail": result}

    @client_router.get("/list/", description="Посмотреть список пользователей")
    async def list(self):
        return {"detail": await self.get_data(UserOrm)}
