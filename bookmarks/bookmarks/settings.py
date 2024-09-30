import os
from pathlib import Path

import dotenv

dotenv.load_dotenv()


def load_bool(key: str, default: str | bool) -> bool:
    value = os.getenv(key=key, default=str(default)).lower()
    return value in ("", "true", "True", "t", "y", "yes", "YES", "1")


def load_list(key: str, default: str | bool) -> list[str]:
    return os.getenv(key=key, default=str(default)).split(",")


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv(key="DJANGO_SECRET_KEY", default="no_key")

DEBUG = load_bool(key="DJANGO_DEBUG", default="False")

ALLOWED_HOSTS = load_list(key="DJANGO_ALLOWED_HOSTS", default="*")

INSTALLED_APPS = [
    "account.apps.AccountConfig",
    "homepage.apps.HomepageConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "bookmarks.urls"

TEMPLATES_DIRS = BASE_DIR / "templates"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIRS],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "bookmarks.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation." "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "account:dashboard"
LOGIN_URL = "account:login"
LOGOUT_REDIRECT_URL = "account:logout"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "account.authentication.EmailAuthBackend",
]
