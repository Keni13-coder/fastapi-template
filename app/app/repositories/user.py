from .base import RepositoryBase, TestRepositoryBase
from app.models.user import User
from app.schemas.user import CreateUser, UpdateUser


class RepositoryUser(RepositoryBase[User, CreateUser, UpdateUser]):
    _model = User


class TestRepositoryUser(TestRepositoryBase[dict, CreateUser, UpdateUser]):
    _model = []
