from dataclasses import dataclass


@dataclass
class MessageSchema:
    """
    Схема сообщения для передачи в RPC сервер, для удобства работы с входящими параметрами
    """

    # id сообщения, для индикации запроса и ответа
    id: str
    # Имя метода, который вызывается на исполнение
    method_name: str
    # Имя очереди в которую будет помещен результат выполнения метода
    reply_to: str
    # Имя очереди которую прослушивает RPC сервер
    receiver: str
    # Параметры для вызываемого метода
    kwargs: dict = None
    # Таймаут, на случай если время на выполнение запроса ограничено
    timeout: int = None


def get_message_schema():
    return MessageSchema
