from typing import Annotated, Union
import abc

from fastapi import Depends, Request, Response

from app.models.user import User
from app.schemas.token import ResponseToken, TokenLoginResponse
from app.schemas.user import ResponseUserSchema, CreateUser
from app.schemas.auth import LoginUser, FormAuth
from app.uow.typing.type_protocol import UOWContextProtocol
from app.services.token import ABCTokenService
from app.services.subdomain.serialize_service import UserEntitySerializer
from app.services.subdomain.hasher_service import HasherInterface
from app.utils.validate_data import data_or_error
from app.exceptions.user_error import AUTHException, RegisterException
from app.exceptions.jwt_error import TokenNotAuthenticatedException
from app.utils.global_dependencies import UOWV1Dep, AccessToken
from app.services.subdomain.jwt_service import DefaultAccessPayload


class ABCUserService(abc.ABC):

    def __init__(
        self,
        token_service: ABCTokenService,
        serializer: UserEntitySerializer,
        hasher_class: HasherInterface,
    ) -> None:
        self._token_service = token_service
        self._serializer = serializer
        self._hasher_class = hasher_class

    @abc.abstractmethod
    async def get_user(self, uow_context: UOWContextProtocol, **filters) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def list_users(self, uow_context: UOWContextProtocol, **filters) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def register_user(
        self, user: CreateUser, uow_context: UOWV1Dep
    ) -> ResponseUserSchema:
        """Метод вызываемый в поинтах, для регистрации пользователя в базе"""
        raise NotImplementedError

    @abc.abstractmethod
    async def login_user(
        self, login_data: Annotated[LoginUser, Depends(FormAuth)], uow_context: UOWV1Dep
    ) -> TokenLoginResponse:
        """Метод вызываемый в поинтах, для аунтификации пользователя и выдачи токенов"""
        raise NotImplementedError

    @abc.abstractmethod
    async def current_user(self,
                           request: Request,
                           authorization: AccessToken,
                           uow_context: UOWV1Dep
                           ) -> Union[ResponseUserSchema, dict]:
        raise NotImplementedError


class UserService(ABCUserService):

    async def get_user(self, uow_context: UOWContextProtocol, **filters) -> Union[ResponseUserSchema, dict]:
        async with uow_context as uow:
            user = await uow.user.get(**filters)
            response = {} or user and self._serializer.to_schema_or_dict(user)
            return response

    async def list_users(
        self,
        uow_context: UOWContextProtocol,
        **filters
    ) -> Union[
            list[ResponseUserSchema],
            list[dict]
    ]:
        async with uow_context as uow:
            users = await uow.user.list(**filters)
            responses = {} or users and self._serializer.to_list_schema(users)
            return responses

    async def register_user(
        self, user: CreateUser, uow_context: UOWV1Dep
    ) -> Union[ResponseUserSchema, dict]:
        async with uow_context as uow:
            if not await uow.user.exists(login=user.login):
                user.password = self._hasher_class.create_hash(user.password)
                new_user = await uow.user.create(user)
                await uow.commit()
                return self._serializer.to_schema_or_dict(new_user)

            raise RegisterException("register_user")

    async def login_user(
        self,
        login_data: Annotated[LoginUser, Depends(FormAuth)],
        uow_context: UOWV1Dep,
        response: Response,
    ) -> TokenLoginResponse:
        async with uow_context as uow:
            user: User = data_or_error(
                data=await uow.user.get(
                    login=login_data.login,
                    password=self._hasher_class.create_hash(
                        login_data.password),
                ),
                error=AUTHException,
                params=("login_user",),
            )
            await uow.close()

            tokens: ResponseToken = await self._token_service.create_pair_tokens(
                user_uid=user.id, uow_context=uow_context
            )
            response.set_cookie(
                key="token",
                value=tokens.refresh_token,
                expires=tokens.expire_refresh,
                httponly=True,
                secure=True,
            )
            return tokens.model_dump(exclude={"refresh_token"})

    async def current_user(
        self,
        request: Request,
        authorization: AccessToken,
        uow_context: UOWV1Dep
    ) -> Union[ResponseUserSchema, dict]:
        payload: DefaultAccessPayload = await self._token_service.jwt_service.decode_token(token=authorization)

        user = data_or_error(
            data=await self.get_user(uow_context=uow_context, id=payload["sub"]),
            error=TokenNotAuthenticatedException,
            params=('current_user',),
            key_params={
                'headers': {"WWW-Authenticate": f"Bearer, authorization={request.url_for('login')} resource={request.base_url}"}
            }
        )
        return self._serializer.to_schema_or_dict(user)
