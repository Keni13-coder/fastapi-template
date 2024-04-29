import abc
from datetime import datetime, timedelta, timezone
from typing import Type
import uuid

from app.exceptions.jwt_error import InvalidTokenException
from app.exceptions.not_found import NotFoundEntity
from app.schemas.token import ResponseToken, TokenSchema
from app.services.jwt_service import ABCJWT, DefaultAccessPayload, DefaultRefreshPayload
from app.core.config import settings
from app.uow.typing.type_protocol import UOWContextProtocol
from app.utils.utc_now import datetime_utc
from app.utils.validate_data import data_or_error


class ABCTokenService(abc.ABC):

    def __init__(self, jwt_service: Type[ABCJWT]) -> None:
        self._jwt_service = jwt_service(
            algorithm=settings.algorithm, secret_key=settings.secret_key
        )

    @abc.abstractmethod
    async def create_pair_tokens(
        self, user_uid: uuid.UUID, uow_context: UOWContextProtocol
    ) -> ResponseToken:
        raise NotImplementedError

    @abc.abstractmethod
    async def refresh_pair_tokens(
        self, access_token: str, refresh_token: str, uow_context: UOWContextProtocol
    ) -> ResponseToken:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_token(self):
        raise NotImplementedError


class TokenService(ABCTokenService):

    async def create_pair_tokens(
        self, user_uid: uuid.UUID, uow_context: UOWContextProtocol
    ) -> ResponseToken:
        jti = uuid.uuid4()
        device_id = uuid.uuid4()
        now = datetime_utc()

        response_tokens = await self._jwt_service.create_access_refresh_jwt(
            device_id=device_id, jti=jti, user_uid=user_uid, now=now
        )

        async with uow_context as uow:
            await uow.token.create(
                obj_in=dict(
                    jti=jti, user_uid=user_uid, device_id=device_id, access_iat=now
                )
            )
            await uow.commit()

        return response_tokens

    async def refresh_pair_tokens(
        self, access_token_encode: str, refresh_token_encode: str, uow_context: UOWContextProtocol
    ) -> ResponseToken:

        payload_access: DefaultAccessPayload = await self._jwt_service.decode_token(
            token=access_token_encode, expired=True
        )
        payload_refresh: DefaultRefreshPayload = await self._jwt_service.decode_token(
            token=refresh_token_encode
        )
        async with uow_context as uow:
            refresh_token: TokenSchema =  data_or_error(
                data=await uow.token.get(jti=payload_refresh["jti"]),
                error=NotFoundEntity,
                params=['refresh_pair_tokens']
            )
           
            refresh_token.access_iat = int(refresh_token.access_iat.timestamp()) # в case не разрешить форматировать

            match payload_access:
                
                case {
                    'sub': refresh_token.user_uid,
                    'device_id': refresh_token.device_id,
                    'iat': refresh_token.access_iat,
                }:
                    ...
                case _:
                    """Дропаем все сесси одного пользователя или двоих"""
                    if not payload_access["sub"] == refresh_token.user_uid:
                            if await uow.token.exists(user_uid=payload_access["sub"]):
                                await uow.token.delete(user_uid=payload_access["sub"])
                                
                    await uow.token.delete(user_uid=refresh_token.user_uid)
                    await uow.commit()
                    raise InvalidTokenException("refresh_pair_tokens")

        jti = uuid.uuid4()
        now = datetime_utc()

        async with uow_context as uow:
            await uow.token.update(
                id=refresh_token.id, obj_in={"jti": jti, "access_iat": now}
            )
            await uow.commit()

        return await self._jwt_service.create_access_refresh_jwt(
            user_uid=refresh_token.user_uid,
            device_id=refresh_token.device_id,
            jti=jti,
            now=now,
            expire_refresh=payload_refresh["exp"],
        )

    async def delete_token(self): ...
