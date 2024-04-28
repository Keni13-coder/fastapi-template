from typing import Any, Generic

from app.uow.session.uow_session import BaseSession


class BaseContext(Generic[BaseSession,]):
    def __init__(
        self, async_session_maker: Any, SessionUow: BaseSession
    ):  # посмотреть какой тип данных у async_session_maker
        self.session_factory = async_session_maker
        self.__UOWFactory = SessionUow

    def __call__(self):
        return self

    async def __aenter__(self) -> BaseSession:
        self.session = self.session_factory()
        self.uow = self.__UOWFactory(session=self.session)
        return self.uow

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.uow.rollback()
        await self.uow.close()
