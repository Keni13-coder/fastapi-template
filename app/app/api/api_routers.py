from app.api.endpoints import user, point_test
from app.core.config import settings
from app.schemas.base import ResponseDefault, ResponseMessage
from app.utils.costum_router import APInfoRouter

api_router = APInfoRouter()

api_router.include_router(user.router, prefix="/user", tags=["User"])
api_router.include_router(point_test.router, prefix="/point", tags=["POINT"])


@api_router.get("/", response_model=ResponseDefault[ResponseMessage])
async def get_info_api():
    return dict(
        detail=[{"message": f"available routes via api {settings.api_v1_str}"}],
    )
