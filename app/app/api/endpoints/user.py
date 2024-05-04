from fastapi import Depends, status

from app.services.initialization_services import user_service
from app.utils.costum_router import APInfoRouter
from app.schemas.user import ResponseUserSchema
from app.api.dependencies import RegisterDep, LoginUser
from app.api.responses import login_responses, register_responses

router = APInfoRouter()


@router.post(
    '/register/',
    status_code=status.HTTP_201_CREATED,
    responses=register_responses
    )
async def register(registred_user: RegisterDep):
    return dict(ditail=registred_user)

@router.post(
    '/login/',
    responses=login_responses
    )
async def login_user(token_data: LoginUser):
    return dict(ditail=token_data)