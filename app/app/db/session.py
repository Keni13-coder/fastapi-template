from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

if settings.MODE.lower() == "test":
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_PARAMS = {}

DATABASE_URL = settings.postgres_url


engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class FakeAsyncSessionMaker:
    is_commit = False
    is_close = False
    is_rollback = False

    def __init__(self) -> None:
        pass

    async def commit(self):
        self.is_commit = True

    async def rollback(self):
        self.is_rollback = True

    async def close(self):
        self.is_close = True
