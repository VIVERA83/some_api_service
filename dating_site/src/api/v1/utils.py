from uuid import uuid4


def create_new_filename(user_id: str, filename: str) -> str:
    """
    Генерирует имя файла на основе user_id и дополнительного uuid, в качестве типа файла берется значение из filename
    :param user_id: строка в прицепе любая но подразумевается uuid
    :param filename: реальное имя файла, требуется type
    :return: новое имя файла
    """
    return "{user_id}_{index}.{type}".format(user_id=user_id, index=uuid4().hex, type=filename.split(".")[1])
