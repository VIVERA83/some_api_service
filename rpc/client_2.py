import asyncio
import os
from time import sleep
import aio_pika
from icecream import ic
from rpc.src.rpc.rpc import RPC

RABBITMQ_URL = "amqp://guest:guest@127.0.0.1:5672"


async def main():
    connection = await aio_pika.connect(RABBITMQ_URL)
    print(connection)
    async with connection:
        channel = await connection.channel()
        rpc = await RPC.create(channel, "response")
        file = open("movies.jpg", mode="rb")
        # result = await rpc.call(receiver="image_service",
        #                         method_name="upload_image",
        #                         kwargs={"fd": file.read(),
        #                                 "text": "privet",
        #                                 "file_name": "movies.jpg"},
        #                         reply_to="response")

        # print(type(result), result)
        result = await rpc.call(receiver="image_service",
                                method_name="download_image",
                                kwargs={"path": "dating_images/movies.jpg"},
                                reply_to="response")
        print(type(result))
        with open("movies111.jpg", "bw") as f:
            f.write(result)



def run_cli():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


if __name__ == "__main__":
    print("Клиент")
    run_cli()
