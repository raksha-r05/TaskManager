from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Task Manager API"
    environment: str = "development"
    debug: bool = True

    # Security
    secret_key: str = "change-me"
    access_token_expires_minutes: int = 60 * 24
    algorithm: str = "HS256"

    # Database
    database_url: str = "sqlite+aiosqlite:///./task_manager.db"

    # CORS
    cors_origins: list[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


