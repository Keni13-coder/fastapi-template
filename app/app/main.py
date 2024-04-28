from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.error_handler.exception_handlers import exception_handlers
from app.core.config import settings
from app.utils.hateoas import setup_header_tags
from app.api import api_routers
from app.middlewares.logger import LoggerMiddleware


def create_app():
    fastapi_app = FastAPI(
        title=settings.project_name,
        openapi_url=f"{settings.api_v1_str}/openapi.json",
        exception_handlers=exception_handlers,
    )

    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,  # Allows all origins
        allow_credentials=True,
        allow_methods=settings.CORS_METHODS,  # Allows all methods
        allow_headers=settings.CORS_HEADERS,  # Allows all headers
    )

    fastapi_app.add_middleware(LoggerMiddleware)
    fastapi_app.include_router(
        api_routers.api_router,
        prefix=settings.api_v1_str,
        dependencies=[Depends(setup_header_tags)],
    )

    return fastapi_app


app = create_app()
