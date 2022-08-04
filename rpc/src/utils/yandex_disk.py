# yadisk_async-1.3.3

import io
from yadisk_async import YaDisk


class YandexDisk:
    def __init__(self, secret: str, token: str):
        self.secret = secret
        self.token = token
        self.disk = YaDisk(secret=secret, token=token)

    async def upload(self, fd: io.BytesIO, file_name: str):
        """Принимает изображение переданное в bytes, наносит текст (text) на картинку, далее изображение сохраняется на
        YandexDisk"""
        await self.disk.upload(fd, "dating_images/" + file_name)

    async def download(self, path: str) -> bytes:
        """Загрузить изображение с диска"""
        file = io.BytesIO()
        await self.disk.download(path, file)
        return file.getvalue()

    async def close(self):
        """Корректное закрытие диска"""
        await self.disk.close()
