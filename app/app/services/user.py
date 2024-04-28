from uuid import UUID
import abc

from app.schemas.user import ResponseUserSchema
from app.uow.typing.type_protocol import UOWContextProtocol


class ABCUserService(abc.ABC):

    @abc.abstractmethod
    async def get_user(self, user_id: UUID, uow_context: UOWContextProtocol) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def list_users(self, uow_context: UOWContextProtocol) -> None:
        raise NotImplementedError


class UserService(ABCUserService):

    @classmethod
    async def get_user(
        cls, user_id: UUID, uow_context: UOWContextProtocol
    ) -> ResponseUserSchema:
        async with uow_context as uow:

            user = await uow.user.get(id=user_id)
        if user:
            return user
        return

    @classmethod
    async def list_users(
        cls, uow_context: UOWContextProtocol
    ) -> list[ResponseUserSchema]:
        async with uow_context as uow:
            return [user for user in await uow.user.list()]
