import sys
from typing import Any, Awaitable, Callable, MutableMapping

from loguru import logger

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.requests import Request

from app.core.config import settings

from app.exceptions.error_server_500 import ServerError


class LoggerMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: Callable[
            [
                MutableMapping[str, Any],
                Callable[[], Awaitable[MutableMapping[str, Any]]],
                Callable[[MutableMapping[str, Any]], Awaitable[None]],
            ],
            Awaitable[None],
        ],
        dispatch: (
            Callable[
                [Request, Callable[[Request], Awaitable[Response]]], Awaitable[Response]
            ]
            | None
        ) = None,
    ) -> None:
        super().__init__(app, dispatch)
        logger.remove()
        logger.add(sys.stderr, colorize=True, format=settings.format)
        logger.add(
            "logs/out.log",
            backtrace=True,
            diagnose=True,
            rotation="1 week",
            compression="zip",
            level="ERROR",
            format=settings.format,
        )
        logger.add(
            "logs/api.log",
            rotation="1 week",
            compression="zip",
            format=settings.format,
            level=settings.log_level,
        )

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        msg = f"{request.method} {request.url.path} {request.query_params}"
        try:
            response = await call_next(request)
            msg += f"| {response.status_code}"
            logger.info(msg)
            return response

        except Exception:
            msg += "| 500 Internal Server Error"
            logger.exception(msg)
        raise ServerError("dispatch")
