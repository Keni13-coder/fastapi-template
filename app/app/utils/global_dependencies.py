from typing import Annotated
from fastapi import Depends
from app.uow.context.uow_context import UOWV1
from app.uow.typing.type_protocol import UOWContextProtocol


UOWV1Dep = Annotated[UOWContextProtocol, Depends(UOWV1)]
