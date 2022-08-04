from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from fastapi import File, UploadFile, Request
from src.models.user_model import UserOrm
from src.api.v1.schema.user_schema import UserModel
from src.api.v1.base_api import BaseAPI
from src.api.v1.schema.validate import validate_file
from icecream import ic

client_router = InferringRouter()

from PIL import Image, ImageDraw, ImageFont
import io
import pickle


def add_watermark(fd, text: str) -> io.BytesIO:
    """
    Добавить к рисунку водные знаки.
    :param fd: файловый дескриптор, либо путь к файлу.
    :param text: текст, который будет наноситься на картинку.
    :return: измененный файловый дескриптор с изображением
    """
    image = Image.open(fd)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 36)
    draw.text((50, 50), text, font=font, align="center", fill=int("8b00ff", 16))
    fd = io.BytesIO()
    fd.name = "font.jpg"
    image.save(fd)
    image.show()
    return fd


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

        add_watermark(file.file, "avatar")
        return {"detail": "ok"}

    @client_router.get("/list/", description="Посмотреть список пользователей")
    async def list(self):
        if users := await self.service.get_data(UserOrm):
            pass

        return {"detail": users}
