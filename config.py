import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


IS_PRODUCTION = _as_bool(os.getenv("RENDER")) or os.getenv("APP_ENV", "development").lower() == "production"


def _upload_folder() -> str:
    configured = Path(os.getenv("UPLOAD_FOLDER", "static/uploads")).expanduser()
    return str(configured if configured.is_absolute() else BASE_DIR / configured)


class Config:
    PRODUCTION = IS_PRODUCTION
    SECRET_KEY = os.getenv("SECRET_KEY") or (None if IS_PRODUCTION else "dev-only-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", f"sqlite:///{(BASE_DIR / 'instance' / 'repair.db').as_posix()}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = _upload_folder()
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 5 * 1024 * 1024))
    WTF_CSRF_TIME_LIMIT = None
    ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = IS_PRODUCTION
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = "Lax"
    REMEMBER_COOKIE_SECURE = IS_PRODUCTION
    TRUST_PROXY_HEADERS = _as_bool(os.getenv("TRUST_PROXY_HEADERS"), IS_PRODUCTION)


class TestConfig(Config):
    TESTING = True
    PRODUCTION = False
    SECRET_KEY = "test-secret-key"
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False
    TRUST_PROXY_HEADERS = False
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

