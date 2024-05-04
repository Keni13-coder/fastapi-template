from typing import Annotated

from fastapi import Depends

from app.services.initialization_services import user_service
from app.schemas.user import ResponseUserSchema
from app.schemas.token import TokenLoginResponse


RegisterDep = Annotated[ResponseUserSchema, Depends(user_service.register_user)]
LoginUser = Annotated[TokenLoginResponse, Depends(user_service.login_user)]


