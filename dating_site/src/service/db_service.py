from fastapi import Depends
from functools import lru_cache
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, ProgrammingError
from asyncpg.exceptions import UndefinedTableError
from sqlalchemy.future import select

from src.models.user_model import MODELS
from src.service.db.postgres import get_session
from icecream import ic


class DBService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def set_data(self, model: MODELS):
        self.session.add(model)
        try:
            await self.session.commit()
        except IntegrityError as errors:
            await self.session.rollback()
            raise errors
        except (UndefinedTableError, ProgrammingError) as errors:
            raise errors

    async def get_data(self, model: MODELS):
        try:
            result = await self.session.execute(select(model))
        except ConnectionRefusedError as e:
            return ic(e)
        return result.scalars().all()


@lru_cache
def get_db_service(session: AsyncSession = Depends(get_session)) -> DBService:
    return DBService(session)
