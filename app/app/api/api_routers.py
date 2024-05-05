from fastapi import APIRouter, Request

from app.api.endpoints import user, point_test
from app.core.config import settings
from app.schemas.base import ResponseDefault, ResponseMessage


api_router = APIRouter()

api_router.include_router(user.router, prefix="/user", tags=["User"])
api_router.include_router(point_test.router, prefix="/point", tags=["POINT"])


@api_router.get("/", response_model=ResponseDefault[ResponseMessage])
async def get_info_api(request: Request):
    return dict(
        detail=[
            {"message": f"available routes via api {settings.api_v1_str}"}
            ],
        info_api=request  
    )
