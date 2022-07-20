from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.models.user_model import MODELS
from functools import lru_cache
from src.db.postgres import get_session

from icecream import ic


class Service:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def set_data(self, model: MODELS):
        self.session.add(model)
        try:
            await self.session.commit()
        except IntegrityError as errors:
            await self.session.rollback()
            raise errors


@lru_cache
def get_service(session: AsyncSession = Depends(get_session)) -> Service:
    return Service(session)

# from src.models.user_model import User
# from src.db.postgres import get_session
# import asyncio
# from icecream import ic
# import re
#
#
# async def main():
#     service = get_service()  # Service(session=get_session())
#
#     user = User(avatar="avatar", sex="man", first_name="First Name", last_name="Last Name", email="email",
#                 password="password")
#     try:
#         await service.set_data(user)
#     except IntegrityError as er:
#         if er.code == "gkpj":
#             err_message = str(er.args[0])
#             result = [str(item) for item in er.params if err_message.count(str(item))]
#     return
#
#
# if __name__ == "__main__":
#     asyncio.run(main=main())
