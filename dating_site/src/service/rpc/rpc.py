# aio_pika-8.1.0
import asyncio

from aio_pika import Queue, Message, IncomingMessage
from aio_pika.abc import AbstractQueue, AbstractChannel
from typing import Optional, Callable, Any
from asyncio import Event, wait_for
from uuid import uuid4
import pickle

from inspect import iscoroutinefunction
from concurrent import futures
import logging

from .schema import MessageSchema


class RPC:
    channel: Optional[AbstractChannel] = None
    # очередь, которую слушаем
    listen_queue: Optional[Queue] = None
    # Словарь методов которые зарегистрированы
    methods: dict[str, Callable] = {}

    # параметры необходимые для call
    response_message: Optional[Message] = None
    flag: Optional[Event] = None  # нужен для того, что бы дожидаться ответа из очереди
    msg: Optional[MessageSchema] = None

    @classmethod
    async def create(cls, channel: AbstractChannel, listen_queue: str) -> "RPC":
        """
        Создаем экземпляр
        :param channel: канал с RabbitMQ server
        :param listen_queue: имя очереди из которою будем слушать
        :return:
        """
        cls.channel = channel
        cls.listen_queue: AbstractQueue = await cls.channel.declare_queue(
            name=listen_queue
        )
        return cls()

    async def register_method(self, method_name: str, method: Callable):
        """
        Регистрация функции обработчика, которая будет вызываться когда будет приходить сообщение с соответствующим
        method_name.
        :param method_name: имя функции, на которое будет срабатывать ее вызов.
        :param method: функция или любой другой объект который можно вызвать.
        :return: None
        """
        if callable(method):
            self.methods[method_name.lower()] = method
        else:
            return TypeError("The passed object is not called")
        await self.listen_queue.consume(callback=self.on_message)  # noqa
        logging.info(f"RPC.register_method: {method_name}")

    async def call(
            self,
            receiver: str,
            method_name: str,
            kwargs: Optional[dict] = None,
            expiration: Optional[int] = None,
            reply_to: str = None,
    ) -> Message:
        """
        Метод, вызывает удаленный метод с названием method_name (вызываемый метод предварительно должен быть
        зарегистрирован через register_method).
        Метод срабатывает при вызове на стороне отправителя сообщения (Клиент)
        :param method_name: имя вызываемого метода.
        :param kwargs: параметры, которые передаются в вызываемую функцию как kwargs, то есть some_method(**kwargs).
        :param expiration: время ожидания ответа, после которого вызывается исключение TimeoutError.
        :param reply_to: очередь в которую вернуть результат, если значение не указано
                         будет использовать очередь для прослушку listen_queue.
        :param receiver: очередь в которую отправляем задание на исполнение.
        :return: Message - сообщение
        """

        async def callback(message: IncomingMessage):
            async with message.process():
                if message.correlation_id == self.msg.id:
                    self.response_message = pickle.loads(message.body)
                    self.flag.set()

        self.flag = Event()  # нужен для того, что бы дожидаться ответа из очереди
        response_queue_flag = Event()  #
        self.msg = MessageSchema(
            uuid4().hex,
            method_name,
            reply_to or self.listen_queue.name,
            receiver,
            kwargs,
            expiration,
        )

        if not response_queue_flag.is_set():
            await self.listen_queue.consume(callback)  # noqa
            response_queue_flag.set()

        await response_queue_flag.wait()
        await self.channel.default_exchange.publish(
            message=self.create_message(self.msg, self.msg.id),
            routing_key=self.msg.receiver,
        )
        await self.flag.wait()
        return self.response_message

    async def on_message(self, message: IncomingMessage) -> None:
        """
        Метод, который вызывается при появлении в очереди новых сообщений. Данный метод вызывает
        и дожидается исполнения нужной функции, полученный результат отправляет в очередь с ответами,
        в случае если метод не найден возвращает ошибку.
        Метод срабатывает на принимающий стороне (Сервер).
        :param message: IncomingMessage
        :return:
        """
        async with message.process():
            body: MessageSchema = pickle.loads(message.body)
            if not body.kwargs:
                body.kwargs = {}
            if func := self.methods.get(body.method_name.lower()):
                try:
                    result = await wait_for(
                        self.run_method(func, **body.kwargs), body.timeout
                    )
                except asyncio.TimeoutError:
                    logging.error(
                        f"RPC.on_message: TimeoutError: {body.method_name}, timeout={body.timeout}"
                    )
                    result = TimeoutError(
                        f"TimeoutError: {body.method_name}, timeout={body.timeout}"
                    )
            else:
                result = KeyError(f"Method name is not defined: {body.method_name}")
                logging.error(
                    f"RPC.on_message: Method name is not defined: {body.method_name}"
                )
            await self.channel.default_exchange.publish(
                message=self.create_message(result, message.correlation_id),
                routing_key=body.reply_to,
            )

    @staticmethod
    def create_message(data: Any, id_message: str) -> Message:
        """
        Создать сообщение для отправки по каналу
        :param data: данные для отправка
        :param id_message: id сообщения
        :return: Message
        """
        return Message(body=pickle.dumps(data), correlation_id=id_message)

    @staticmethod
    async def run_method(func: Callable, **kwargs) -> Any:
        """
        Запускает переданный вызываемый объект в соответствии от типа, если объект не поддерживает асинхронный запуск
        он запускается в отдельном пуле. В случае возникновения ошибки в процессе исполнения объекта будет
        возвращено исключение.
        :param func: Любой объект который можно вызвать. Пример: foo()
        :param kwargs: именованные атрибуты для запуска. Пример: foo(**kwargs)
        :return: какой-то результат
        """
        try:
            if iscoroutinefunction(func):
                if kwargs:
                    return await func(**kwargs)
                else:
                    return await func()
            elif kwargs:
                with futures.ProcessPoolExecutor() as pool:
                    return await asyncio.get_event_loop().run_in_executor(
                        pool, func, *kwargs.values()
                    )
            else:
                with futures.ProcessPoolExecutor() as pool:
                    return await asyncio.get_event_loop().run_in_executor(pool, func)
        except Exception as e:
            # конкретную ошибку не отследить так как она зависит от вызываемого метода,
            # который может быть чем угодно
            logging.error(
                f"RPC.on_message: error during execution of the called object '{func.__name__}': : {str(e)}"
            )
            return e

