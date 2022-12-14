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
    # Имя очереди которую прослушивает RPC сервер (куда кладем запрос на исполнение)
    receiver: str
    # Параметры для вызываемого метода
    kwargs: dict = None
    # Таймаут, на случай если время на выполнение запроса ограничено
    timeout: int = None

    @property
    def get_dict(self):
        return {
            "id": self.id,
            "method_name": self.method_name,
            "reply_to": self.reply_to,
            "receiver": self.receiver,
            "kwargs": self.kwargs,
            "timeout": self.timeout,
        }
