from app.db.session import async_session_maker, FakeAsyncSessionMaker
from app.uow.context.base import BaseContext
from app.uow.session.uow_session import FakeSessionByUOW, SessionByUOW


class UOWContext(BaseContext[SessionByUOW]):
    pass


class FakeUOWContext(BaseContext[FakeSessionByUOW]):
    pass


UOWV1 = UOWContext(async_session_maker, SessionByUOW)

FakeUOW = FakeUOWContext(FakeAsyncSessionMaker, FakeSessionByUOW)
