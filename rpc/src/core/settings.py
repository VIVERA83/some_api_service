import io

from src.core.config import settings
from rpc.src.utils.yandex_disk import YandexDisk
from rpc.src.utils.watermark import add_watermark

ya_disk = YandexDisk(secret=settings.ya.ya_secret, token=settings.ya.ya_token)


async def upload_image(fd: bytes, file_name: str, text: str, font: str = "Kabaret.ttf", font_size: int = 36):
    """
    Загрузить изображение в yandex, предварительно нанести надпись на изображение
    :param fd: Изображение в виде bytes.
    :param file_name: Имя файла под каким будет хранится в облаке
    :param text: Надпись, которую будем наносить на изображение
    :param font: Шрифт
    :param font_size: Размер шрифта
    :return:
    """
    file = io.BytesIO(add_watermark(fd, text, font, font_size))
    return await ya_disk.upload(file, file_name)


async def download_image(path: str) -> bytes:
    """
    Скачать с yandex disk
    :param path: Путь на yandex_disk К файлу который будет скачен
    :return: Файл в виде байтов
    """
    return await ya_disk.download(path)
