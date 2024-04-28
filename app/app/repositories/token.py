from .base import RepositoryBase, TestRepositoryBase
from app.models.token import Token
from app.schemas.token import RefreshToken, UpdateTokens


class RepositoryToken(RepositoryBase[Token, RefreshToken, UpdateTokens]):
    _model = Token


class TestRepositoryToken(TestRepositoryBase[list, RefreshToken, UpdateTokens]):
    _model = []
