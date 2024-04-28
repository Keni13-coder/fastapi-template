from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.error_server_500 import ServerError


async def server_error(request: Request, exc: Exception):
    class_erorr = ServerError() if not isinstance(exc, ServerError) else exc
    return JSONResponse(
        status_code=class_erorr.status_code,
        content=class_erorr.detail,
    )
