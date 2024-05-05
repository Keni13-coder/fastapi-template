from typing import Union
from fastapi import Depends, Request, status, APIRouter

from app.schemas.user import ResponseUserSchema
from app.schemas.token import TokenLoginResponse
from app.schemas.base import ResponseDefault,  ResponseWithParams
from app.api.dependencies import RegisterDep, LoginUser, OffsetLimitParam
from app.utils.global_dependencies import UOWV1Dep
from app.api.responses import login_responses, register_responses
from app.services.initialization_services import user_service

router = APIRouter()


@router.post(
    "/register/",
    status_code=status.HTTP_201_CREATED,
    responses=register_responses,
    response_model=ResponseDefault[ResponseUserSchema]
)
async def register(request: Request, registred_user: RegisterDep):
    return dict(
        detail=[registred_user],
        info_api=request
        )


@router.post(
    "/login/",
    responses=login_responses,
    response_model=ResponseDefault[TokenLoginResponse]
    )
async def login(request: Request, token_data: LoginUser):
    return dict(
        detail=[token_data],
        info_api=request
        )

@router.get('/get-one/')
async def get_one(request: Request, current_user, uow_context: UOWV1Dep):
    ...
    
@router.get(
    '/get-all/',
    response_model=ResponseWithParams[
        Union[
            ResponseUserSchema,
            dict
            ]
        ]
    )
async def get_all(request: Request, params: OffsetLimitParam, uow_context: UOWV1Dep):
    params = params.model_dump()
    response = await user_service.list_users(uow_context=uow_context, **params)
    return dict(
        detail=response,
        info_api=request,
        params=params
        )