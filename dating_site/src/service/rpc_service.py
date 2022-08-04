from fastapi import Depends
from typing import Optional
import aio_pika
from aio_pika.abc import AbstractConnection, AbstractChannel
from functools import lru_cache

from .rpc.rpc import RPC
from src.core.config import settings


class RPCService:
    connection: Optional[AbstractConnection] = None
    channel: Optional[AbstractChannel] = None
    client_rpc: Optional[RPC] = None

    @classmethod
    async def create(cls) -> "RPCService":
        cls.connection = await aio_pika.connect(settings.rpc.rabbit_dsn)
        cls.channel = await cls.connection.channel()
        cls.client_rpc = await RPC.create(cls.channel, "image_service", )
        return cls()

    async def call(self, receiver: str, method_name: str, kwargs: dict, expiration: int = None, reply_to: str = None):
        return await self.client_rpc.call(receiver, method_name, kwargs, expiration, reply_to)

    async def close(self):
        await self.connection.close()


@lru_cache
def get_rpc_service(rpc_service: RPCService = Depends(RPCService.create)) -> RPCService:
    return rpc_service
