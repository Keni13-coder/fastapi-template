from typing import Annotated

from fastapi import FastAPI, Depends, Header, Request, APIRouter


app = FastAPI()
main_router = APIRouter()
router = APIRouter()
fake_router = APIRouter()


@fake_router.get("/create-post/")
async def create(request: Request):
    return {"message": [request.base_url, request.url_for("login")]}


@router.get("/login/")
async def login():
    return {"message": "login"}


@app.get("/test/")
async def get_test(request: Request):
    return {"message": [request.base_url, request.url_for("login")]}


main_router.include_router(router, prefix="/user")
main_router.include_router(fake_router, prefix="/post")

app.include_router(router=main_router)
