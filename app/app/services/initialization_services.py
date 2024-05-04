from .user import UserService
from .token import TokenService
from .subdomain.hasher_service import Hasher
from .subdomain.jwt_service import JWTService
from .subdomain.serialize_service import TokenEntitySerializer, UserEntitySerializer
from app.schemas.token import TokenSchema
from app.schemas.user import ResponseUserSchema


serializer_token = TokenEntitySerializer(serialize_schema=TokenSchema)
serializer_user = UserEntitySerializer(serialize_schema=ResponseUserSchema)

token_service = TokenService(jwt_service=JWTService, serializer=serializer_token)
user_service = UserService(
    token_service=token_service, serializer=serializer_user, hasher_class=Hasher()
)
