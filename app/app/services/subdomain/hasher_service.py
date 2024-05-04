import abc
import json
from typing import Any, Protocol
import hashlib

from app.core.config import settings


class HasherInterface(Protocol):

    def __init__(self) -> None: ...

    def create_hash(self, value: Any) -> str: ...

    def verify_hash(self, verify_value: Any, hashed_value: str) -> bool: ...


class Hasher:

    def __init__(self) -> None:
        self._salt = settings.secret_key.encode()

    def _create_hash(self, value: Any) -> str:

        if not isinstance(value, str):
            value = json.dumps(value, default=str)
        return hashlib.scrypt(
            password=value.encode(), salt=self._salt, n=8, r=512, p=4, dklen=32
        ).hex()

    def create_hash(self, value: Any) -> str:
        return self._create_hash(value)

    def verify_hash(self, verify_value: Any, hashed_value: str):

        verify_value_hash = self._create_hash(verify_value)
        return verify_value_hash == hashed_value
