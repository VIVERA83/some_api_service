from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

from src.models.user_model import UserOrm
from src.api.v1.schema.user_schema import UserModel
from src.api.v1.base_api import BaseAPI

client_router = InferringRouter()


@cbv(client_router)
class ClientApi(BaseAPI):

    @client_router.post("/create/",
                        description="Зарегистрировать нового пользователя")
    async def create(self, user: UserModel):
        """Create a new client"""
        await self.set_data(UserOrm(**user.dict()))
        return {"detail": "ok"}
