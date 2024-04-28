from typing import Protocol, Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import user, token


class SessionProtocol(Protocol):
    def __init__(self) -> None:
        self.session: AsyncSession
        self.user: Type[user.RepositoryUser]
        self.token: Type[token.RepositoryToken]

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def close(self):
        await self.session.close()


class UOWContextProtocol(Protocol):

    async def __aenter__(self):
        return SessionProtocol()

    async def __aexit__(self, exc_type, exc_val, exc_tb): ...
