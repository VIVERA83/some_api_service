# yadisk_async-1.3.3

import io
from yadisk_async import YaDisk


class YandexDisk:
    def __init__(self, secret: str, token: str):
        self.secret = secret
        self.token = token
        self.disk = YaDisk(secret=secret, token=token)

    async def upload(self, fd: io.BytesIO, file_name: str):
        """
        Принимает изображение переданное в bytes, наносит текст (text) на картинку, далее изображение сохраняется на
        YandexDisk.
        :param fd: Файл, в виде байтового объекта.
        :param file_name: Имя файла, под которым будет хранится файл в Yandex Disk.
        :return:
        """
        await self.disk.upload(fd, "dating_images/" + file_name)

    async def download(self, path: str) -> bytes:
        """
        Загрузить изображение с диска
        :param path: Путь к файлу в Yandex Disk
        :return: файл в виде bytes
        """
        file = io.BytesIO()
        await self.disk.download(path, file)
        return file.getvalue()

    async def close(self):
        """Корректное закрытие соединений с диском"""
        await self.disk.close()
