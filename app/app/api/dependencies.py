from typing import Annotated

from fastapi import Depends, Response

from app.services.initialization_services import user_service, token_service
from app.schemas.user import ResponseUserSchema
from app.schemas.token import ResponseToken, TokenLoginResponse
from app.schemas.base import Params

from app.utils.global_dependencies import UOWV1Dep, AccessToken, RefreshToken
from app.services.initialization_services import token_service

RegisterUser = Annotated[ResponseUserSchema, Depends(user_service.register_user)]
LoginUser = Annotated[TokenLoginResponse, Depends(user_service.login_user)]
CurrentUser = Annotated[ResponseUserSchema, Depends(user_service.current_user)]
OffsetLimitParam = Annotated[Params, Depends()]


# RefreshTokenDep
async def refresh_token(
    response: Response,
    authorization: AccessToken,
    token: RefreshToken,
    uow_context: UOWV1Dep,
) -> TokenLoginResponse:
    new_pair_tokens: ResponseToken = await token_service.refresh_pair_tokens(
        access_token_encode=authorization,
        refresh_token_encode=token,
        uow_context=uow_context,
    )
    response.set_cookie(
        key="token",
        value=new_pair_tokens.refresh_token,
        expires=new_pair_tokens.expire_refresh,
        httponly=True,
        secure=True,
    )

    return new_pair_tokens.model_dump(exclude={"refresh_token"})


RefreshTokenDep = Annotated[TokenLoginResponse, Depends(refresh_token)]
