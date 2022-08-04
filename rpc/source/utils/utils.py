# Pillow - 9.2.0
import io
import logging
from PIL import Image, ImageDraw, ImageFont  # noqa
from functools import wraps
from time import sleep

TYPE = {"JPEG": "jpg", "PNG": "png"}


def add_watermark(
        fd: bytes, text: str, font: str = "Kabaret.ttf", font_size: int = 36
) -> bytes:
    """
    Принимает картинку в виде byte и добавляет в нее водяные знаки в виде теста,
    далее возвращает картинку в том же формате.
    :param fd: Изображение в bytes
    :param text: сообщение которое нужно наложить на картинку.
    :param font: шрифт будущего сообщения, путь к файлу со шрифтом.
    :param font_size: размер шрифта.
    :return: видоизмененная картинка типа bytes
    """
    image = Image.open(io.BytesIO(fd))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font, font_size)
    draw.text((50, 50), text, font=font, align="center", fill=int("8b00ff", 16))
    newfile = io.BytesIO()
    newfile.name = "image." + TYPE[image.format]
    image.save(newfile)
    return newfile.getvalue()


def before_execution(sleep_time=2, limit_repeat=50, logging_level=logging.ERROR):
    """
    Декоратор, пытается выполнить декапированную функцию.
    :param sleep_time: Время сна между попытками запуска
    :param limit_repeat: Количество попыток запустить функцию
    :param logging_level: Уровень для сообщения
    :return:
    """
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            limit = limit_repeat
            sec = sleep_time
            while limit:
                try:
                    func(*args, **kwargs)
                    logging.log(logging_level, "  before_execution, Completed")
                    break
                except KeyboardInterrupt:
                    logging.log(logging_level, "  before_execution, Canceled user")
                    break
                except Exception as ex:
                    logging.log(logging_level, f" before_execution, {ex}")
                logging.log(logging_level, f" before_execution, We continue to try to run, remained "
                                           f"{limit} try")
                limit -= 1
                sleep(sec)

        return inner

    return func_wrapper
