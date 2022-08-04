import asyncio
import aio_pika
from aio_pika.abc import AbstractConnection

from source.rpc.rpc import RPC
from source.core.settings import upload_image, download_image, ya_disk
from source.core.config import settings


async def init_rpc() -> AbstractConnection:
    connection = await aio_pika.connect(url=settings.rabbit.rabbit_dsn)
    channel = await connection.channel()
    service = await RPC.create(channel, settings.rpc.queue_name)
    # регистрация функций которые можно будет вызывать
    await service.register_method("upload_image", upload_image)
    await service.register_method("download_image", download_image)
    return connection


def run_server():
    loop = asyncio.get_event_loop()
    connection = loop.run_until_complete(init_rpc())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(connection.close())
        loop.run_until_complete(ya_disk.close())
    finally:
        loop.run_until_complete(connection.close())
