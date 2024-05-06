from fastapi import APIRouter, Request, Response

from app.api.dependencies import RefreshTokenDep, UOWV1Dep, AccessToken, token_service
from app.schemas.base import ResponseDefault, ResponseMessage
from app.schemas.token import TokenLoginResponse
from app.api.responses import refresh_responses, logout_responses

router = APIRouter()


@router.post(
    '/refresh/',
    response_model=ResponseDefault[TokenLoginResponse],
    responses=refresh_responses
)
async def refresh_token(
    request: Request,
    token_data: RefreshTokenDep
    ):
    return dict(
        detail=[token_data],
        info_api=request
    )

@router.delete(
    '/logout/',
    response_model=ResponseDefault[ResponseMessage],
    responses=logout_responses
)
async def logout(
    request: Request,
    response: Response,
    uow_context: UOWV1Dep,
    authorization: AccessToken
    ):
    await token_service.delete_token(access_token_encode=authorization, uow_context=uow_context)
    response.delete_cookie('token', httponly=True, secure=True)
    
    return dict(
        detail=[
            {"message": 'Token was successfully deleted'}
            ],
        info_api=request  
    )