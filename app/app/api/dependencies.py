from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.uow.context.uow_context import UOWV1, BaseContext
from app.services.user import UserService, ABCUserService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_v1_str}/login")

UOWV1Dep = Annotated[BaseContext, Depends(UOWV1)]
UserServiceV1Dep = Annotated[ABCUserService, Depends(UserService)]
