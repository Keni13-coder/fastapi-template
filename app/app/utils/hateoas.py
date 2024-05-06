from fastapi import Request
from fastapi.routing import APIRoute
from app.core.config import settings


def hateoas_gener(request: Request) -> tuple:
    path = request.url.path
    results = set()
    tags = request.scope["route"].tags
    is_main_path = True if path == f"{settings.api_v1_str}/" else False

    for route in request.scope["app"].routes:
        if isinstance(route, APIRoute) and (is_main_path or tags == route.tags):
            method = tuple(route.methods)[0]
            results.add(f"{method}{route.path}")
    return tuple(results)
