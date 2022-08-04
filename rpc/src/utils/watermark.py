# Pillow - 9.2.0
import io
from PIL import Image, ImageDraw, ImageFont  # noqa

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
