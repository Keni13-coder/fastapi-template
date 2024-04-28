from typing import TypeVar, Union

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import FakeAsyncSessionMaker
from app.uow.session.base import DefaultSessionPackMixin, ABCUoW

from app.repositories import user, token


class SessionByUOW(DefaultSessionPackMixin, ABCUoW):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user = user.RepositoryUser(session=self.session)
        self.token = token.RepositoryToken(session=self.session)


class FakeSessionByUOW(DefaultSessionPackMixin, ABCUoW):

    def __init__(self, session: FakeAsyncSessionMaker) -> None:
        self.session = session
        self.user = user.TestRepositoryUser(session=self.session)
        self.token = token.TestRepositoryToken(session=self.session)


BaseSession = TypeVar("BaseSession", bound=Union[SessionByUOW, FakeSessionByUOW])
