# yadisk_async-1.3.3

import io
from yadisk_async import YaDisk
from source.utils.utils import add_watermark
from source.core.config import settings


class YandexDisk:
    def __init__(self, secret: str, token: str):
        self.secret = secret
        self.token = token
        self.disk = YaDisk(secret=secret, token=token)

    async def upload(
            self,
            fd: bytes,
            file_name: str,
            text: str,
            font: str = None,
            font_size: int = None,
    ) -> str:
        """
        Принимает изображение переданное в bytes, наносит текст (text) на картинку, далее изображение сохраняется на
        YandexDisk.
        :param fd: Файл, в виде байтового объекта.
        :param file_name: Имя файла, под которым будет хранится файл в Yandex Disk.
        :param text: Надпись на изображение.
        :param font: Путь к файлу с шрифтами.
        :param font_size: Размер шрифта.
        :return: Ссылка на загрузку файла из облако.
        """
        file = io.BytesIO(add_watermark(fd, text, font, font_size))
        await self.disk.upload(file, "dating_images/" + file_name)
        return await self.disk.get_download_link("dating_images/" + file_name)

    async def download(self, path: str) -> bytes:
        """
        Загрузить изображение с диска
        :param path: Путь к файлу в Yandex Disk
        :return: Файл в виде bytes
        """
        file = io.BytesIO()
        await self.disk.download(path, file)
        return file.getvalue()

    async def close(self):
        """Корректное закрытие соединений с диском"""
        await self.disk.close()


ya_disk = YandexDisk(secret=settings.ya.ya_secret, token=settings.ya.ya_token)


async def upload_image(
        fd: bytes, file_name: str, text: str, font: str = None, font_size: int = None
) -> str:
    """
    Загрузить изображение в yandex, предварительно нанести надпись на изображение
    :param fd: Изображение в виде bytes.
    :param file_name: Имя файла под каким будет хранится в облаке
    :param text: Надпись, которую будем наносить на изображение
    :param font: Шрифт
    :param font_size: Размер шрифта
    :return: Ссылка на загрузку файла из облако.
    """
    return await ya_disk.upload(fd, file_name, text, font, font_size)


async def download_image(path: str) -> bytes:
    """
    Скачать с yandex disk
    :param path: Путь на yandex_disk К файлу который будет скачен
    :return: Файл в виде байтов
    """
    return await ya_disk.download(path)
