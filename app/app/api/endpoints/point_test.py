from typing import Annotated
from fastapi import APIRouter, Body, Depends, Form, HTTPException, status, UploadFile
from app.api.dependencies import UOWV1Dep
from app.utils.create_responses import create_responses_for_point
from app.api.responses_errors import not_found_400
from app.schemas.base import ResponseDefault, ResponseMessage
from app.utils.costum_router import APInfoRouter
from app.services.user import UserService

router = APInfoRouter()


@router.post(
    "/test-annotation/",
    response_model=ResponseDefault[ResponseMessage],
    responses=create_responses_for_point(not_found_400),
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
