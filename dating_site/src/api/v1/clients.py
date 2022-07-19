from fastapi import Request
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from src.api.v1.schema.user_schema import UserModel

client_router = InferringRouter()


@cbv(client_router)
class ClientApi:

    @client_router.post("/create/",
                        description="Зарегистрировать нового пользователя")
    async def create(self, request: Request, user: UserModel):
        """Create a new client"""

        return user
