import secrets

from enum import Enum

from pydantic import PostgresDsn, Field, computed_field, field_validator
from pydantic_settings import BaseSettings


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class StatusMode(str, Enum):
    TEST = "test"
    DEV = "dev"


class Settings(BaseSettings):
    """Настройки проекта"""

    MODE: StatusMode = Field(title="Статус разработки", default=StatusMode.DEV)

    api_v1_str: str = Field(title="Prefix для V1", default="/api/v1")
    debug: bool = Field(title="Режим отладки", default=True)
    format: str = Field(
        title="формат для logger",
        default="<level>{level}</level> | <magenta>{time:%Y-%m-%d %H:%M:%S}</magenta> | <level>{message}</level>",
    )
    secret_key: str = Field(
        title="Секретный ключ", default_factory=lambda: secrets.token_hex(16)
    )
    algorithm: str = Field(default="HS256")
    log_level: str = Field(title="Уровень логирования", default=LogLevel.DEBUG)
    project_name: str = Field(
        title="Имя проекта", default="Unnamed", alias="PROJECT_SLUG"
    )

    # region Настройки БД
    postgres_user: str = Field(title="Пользователь БД")
    postgres_password: str = Field(title="Пароль БД")
    postgres_host: str = Field(title="Хост БД")
    postgres_port: int = Field(title="Порт ДБ", default="5432")
    postgres_db: str = Field(title="Название БД")
    # endregion

    # region JWT
    algorithm: str = Field(default="HS256")
    expired_access: float = Field(default=30.0, description="30 минут")
    expired_refresh: float = Field(default=20160.0, description="14 дней")

    # region CORS проверить как передавать список строк в env
    CORS_HEADERS: list[str] = Field(
        default=[
            "Content-Type",
            "Set-Cookie",
            "Access-Control-Allow-Headers",
            "Access-Control-Allow-Origin",
            "Authorization",
            "Router-Tags",  # надо проверить рабоатет ли, потому что записано через маленькие в добавлении `router-tags`
        ],
        title="Допустимые заголовки",
    )
    CORS_ORIGINS: list[str] = Field(
        default=["https://www.youtube.com/"],  # проверить нужно ли добавлять порт
        title="Допустимые сервера для подключения",
    )
    CORS_METHODS: list[str] = Field(
        default=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
        title="Допустимые http методы",
    )
    # endregion

    @computed_field
    @property
    def postgres_url(self) -> PostgresDsn:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.postgres_user,
                password=self.postgres_password,
                host=self.postgres_host,
                port=self.postgres_port,
                path=self.postgres_db,
            )
        )

    class Config:
        env_file = ".env"


settings = Settings()
