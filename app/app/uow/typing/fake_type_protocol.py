from typing import Protocol, Type
from app.repositories import user, token
from app.db.session import FakeAsyncSessionMaker


class FakeSessionProtocol(Protocol):
    def __init__(self) -> None:
        self.session: FakeAsyncSessionMaker
        self.user: user.TestRepositoryUser
        self.token: token.TestRepositoryToken

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def close(self):
        await self.session.close()


class FakeUOWContextProtocol(Protocol):
    async def __aenter__(self):
        return FakeSessionProtocol()

    async def __aexit__(self, exc_type, exc_val, exc_tb): ...
