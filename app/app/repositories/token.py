from .base import RepositoryBase, TestRepositoryBase
from app.models.token import Token
from app.schemas.token import RefreshToken, UpdateTokens


class RepositoryToken(RepositoryBase[Token, RefreshToken, UpdateTokens]):
    _model = Token


class TestRepositoryToken(TestRepositoryBase[dict, RefreshToken, UpdateTokens]):
    _model = []
