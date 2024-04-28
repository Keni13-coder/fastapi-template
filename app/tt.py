import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings

now = datetime.now(timezone.utc)
data = {
    "sub": "123456",
    "device_id": "12345dsda",
    "exp": now + timedelta(days=30),
    "nfb": str(now),
}


encode_data = jwt.encode(
    payload=data, key=settings.secret_key, algorithm=settings.algorithm
)
decode_data = jwt.decode(
    jwt=encode_data, key=settings.secret_key, algorithms=[settings.algorithm]
)

exp: datetime = now + timedelta(days=30)


print(exp.timestamp())

print(decode_data)
