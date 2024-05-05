from typing import Annotated
from fastapi import APIRouter, Body, Depends, Form, HTTPException, status, UploadFile
from app.utils.global_dependencies import UOWV1Dep

from app.schemas.base import ResponseDefault, ResponseMessage
from app.services.user import UserService

router = APIRouter()


@router.post(
    "/test-annotation/",
    response_model=ResponseDefault[ResponseMessage],
)
async def annot(uowv1: UOWV1Dep):
    await UserService.list_users(uowv1)
    return dict(detail=[{"message": "ok"}])


@router.post("/create-image/")
async def load_image(image: UploadFile):
    return {"message": image.filename}


@router.post("/create-data/")
async def load_image(data=Form(default={"id": 14})):
    return {"message": data}
