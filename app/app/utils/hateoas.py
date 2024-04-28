import json
from typing import Awaitable, Callable
from fastapi import Request, Response
from starlette.responses import JSONResponse
from fastapi.routing import APIRoute
from app.core.config import settings


async def setup_header_tags(request: Request):
    scope = request.scope

    route = scope["route"]
    tags = json.dumps(route.tags).encode()

    headers = scope["headers"]
    headers.append((b"router-tags", tags))


async def hateoas_dict(request: Request):
    path = request.url.path
    is_main_path = True if path == f"{settings.api_v1_str}/" else False
    routes = request.app.routes
    try:
        tags = json.loads(request.headers.get("router-tags"))

    except TypeError:
        return

    response_dict = dict()
    for router in routes:
        if isinstance(router, APIRoute) and (is_main_path or tags == router.tags):
            method = tuple(router.methods)[0]

            response_dict.update(
                {
                    f"{method}{router.path}": {
                        "is_cache": True if "GET" == method else False
                    }
                }
            )
    return response_dict


class ApiInfo(APIRoute):
    async def custom_route_handler(self, request: Request) -> Response:
        response: JSONResponse = await super().get_route_handler()(request)
        api_info = await hateoas_dict(request)
        reponse_data = json.loads(response.body.decode())
        reponse_data.update({"info_api": api_info})
        response.body = json.dumps(reponse_data).encode()
        response.headers["content-length"] = str(len(response.body))
        return response

    def get_route_handler(self) -> Awaitable:
        async def custom_route_handler(request: Request) -> Response:
            return await self.custom_route_handler(request)

        return custom_route_handler
