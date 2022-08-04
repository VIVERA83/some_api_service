from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from fastapi import File, UploadFile, Request
from src.models.user_model import UserOrm
from src.api.v1.schema.user_schema import UserModel
from src.api.v1.base_api import BaseAPI
from src.api.v1.schema.validate import validate_file
from icecream import ic

client_router = InferringRouter()


@cbv(client_router)
class ClientApi(BaseAPI):
    @client_router.post("/create/", description="Зарегистрировать нового пользователя")
    async def create(self, request: Request, user: UserModel):
        """Create a new client"""
        await self.set_data(UserOrm(**user.dict()))
        return {"detail": "ok"}

    @client_router.post(
        "/upload_avatar/", description="Загрузить аватар пользователя пользователя"
    )
    async def upload_avatar(self, file: UploadFile | None = File()):
        await validate_file(file)

        return {"detail": "ok"}

    @client_router.get("/list/", description="Посмотреть список пользователей")
    async def list(self):
        if users := await self.db_service.get_data(UserOrm):
            pass

        return {"detail": users}
