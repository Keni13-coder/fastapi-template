import abc
from typing import Optional, TypedDict
from datetime import datetime, timedelta, timezone
import uuid

from fastapi.security.utils import get_authorization_scheme_param
import jwt

from app.core.config import settings
from app.schemas.token import ResponseToken
from app.utils.utc_now import datetime_utc
from app.utils.format_str_in_uuid import format_to_str_or_nothing
from app.exceptions.jwt_error import (
    InvalidTokenException,
    TokenExpiredException,
    TokenNotAuthenticatedException,
)


class DefaultPayload(TypedDict):
    sub: uuid.UUID
    iat: datetime
    exp: datetime


class DefaultRefreshPayload(DefaultPayload):
    jti: uuid.UUID


class DefaultAccessPayload(DefaultPayload):
    device_id: uuid.UUID


class ABCJWT(abc.ABC):
    def __init__(self, algorithm: str, secret_key: str) -> None:
        self._algorithm = algorithm
        self._secret_key = secret_key

    @abc.abstractmethod
    async def decode_token(self, token: str, expired=False) -> dict:
        """
        Декодирование jwt.

        :param bool expired: Позволяет декодировать истекший токен.
        :return: decoding the token payload
        :rtype: dict
        :raise HTTPException.TokenNotAuthenticatedException: Error, Not authenticated
        :raise HTTPException.InvalidTokenException: Error, invalid token
        :raise HTTPException.TokenExpiredException: Error, the token must be expired
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def create_accsess_jwt(
        self, device_id: uuid.UUID, user_uid: uuid.UUID, iat: datetime, exp: datetime
    ) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    async def create_refresh_jwt(
        self, jti: uuid.UUID, user_uid: uuid.UUID, iat: datetime, exp: datetime
    ) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    async def create_access_refresh_jwt(
        self,
        *,
        device_id: uuid.UUID,
        jti: uuid.UUID,
        user_uid: uuid.UUID,
        now: datetime,
        expire_refresh: Optional[int] = None
    ) -> ResponseToken:
        """Созадние двух токенов доступа и обновления

        :param expire_refresh: Позволяет задать существующий expire для refresh токена
        :type expire_refresh: int or None
        :return: tokens
        :rtype: ResponseToken
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def is_latest_refresh(self, refresh_exp: int) -> bool:
        raise NotImplementedError


class JWTService(ABCJWT):

    async def _create_token(self, payload: dict):
        return "Bearer " + jwt.encode(
            payload=payload, key=self._secret_key, algorithm=self._algorithm
        )

    async def _decode_token_in_option(self, token: str, **options) -> dict:
        scheme, param = get_authorization_scheme_param(token)
        if not token or scheme.lower() != "bearer":
            raise TokenNotAuthenticatedException(
                headers={"WWW-Authenticate": "Bearer"},
            )
        try:
            return jwt.decode(
                jwt=param,
                key=self._secret_key,
                algorithms=[self._algorithm],
                options=options,
            )
        except jwt.exceptions.PyJWTError as ex:
            raise InvalidTokenException("decode_token_in_option")

    async def _create_default_payload(
        self, user_uid: uuid.UUID, iat: datetime, exp: datetime
    ):
        return {"sub": str(user_uid), "iat": iat, "exp": exp}

    async def create_accsess_jwt(
        self, device_id: uuid.UUID, user_uid: uuid.UUID, iat: datetime, exp: datetime
    ) -> str:
        payload = await self._create_default_payload(user_uid, iat, exp)
        payload.update({"device_id": str(device_id)})
        return await self._create_token(payload)

    async def create_refresh_jwt(
        self, jti: uuid.UUID, user_uid: uuid.UUID, iat: datetime, exp: datetime
    ) -> str:
        payload = await self._create_default_payload(user_uid, iat, exp)
        payload.update({"jti": str(jti)})
        return await self._create_token(payload)

    async def decode_token(self, token: str, expired=False) -> dict:
        """
        Декодирование jwt.

        :param bool expired: Позволяет декодировать истекший токен.
        """
        result_payload = {}

        if expired:
            payload = await self._decode_token_in_option(token=token, verify_exp=False)

            if payload["exp"] < datetime_utc().timestamp():
                result_payload = payload
            else:
                raise TokenExpiredException("decode_token")
        else:
            result_payload = await self._decode_token_in_option(token=token)

        return format_to_str_or_nothing(result_payload)

    async def create_access_refresh_jwt(
        self,
        *,
        device_id: uuid.UUID,
        jti: uuid.UUID,
        user_uid: uuid.UUID,
        now: datetime,
        expire_refresh: Optional[int] = None
    ) -> ResponseToken:
        """Созадние двух токенов доступа и обновления

        :param expire_refresh: Позволяет задать существующий expire для refresh токена
        :type expire_refresh: int or None
        """

        access_token = await self.create_accsess_jwt(
            device_id=device_id,
            user_uid=user_uid,
            iat=now,
            exp=now + timedelta(minutes=settings.expired_access),
        )
        exp = expire_refresh or now + timedelta(minutes=settings.expired_refresh)
        refresh_token = await self.create_refresh_jwt(
            jti=jti, user_uid=user_uid, iat=now, exp=exp
        )

        return ResponseToken(
            access_token=access_token, refresh_token=refresh_token, expire_refresh=exp
        )

    async def is_latest_refresh(self, refresh_exp: int) -> bool:
        return refresh_exp > int(
            (datetime_utc() + timedelta(minutes=settings.expired_access)).timestamp()
        )
