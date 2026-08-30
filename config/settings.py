import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-poc-employer-first-dev-only-key"
)
DEBUG = os.environ.get("DEBUG", "True").lower() in ("1", "true", "yes")
ON_VERCEL = bool(os.environ.get("VERCEL"))

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "ALLOWED_HOSTS",
        "localhost,127.0.0.1,.vercel.app",
    ).split(",")
    if host.strip()
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Vercel Functions have a read-only filesystem except /tmp.
_default_db = (
    "sqlite:////tmp/firstpass-poc.sqlite3"
    if ON_VERCEL
    else f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
)
DATABASES = {
    "default": dj_database_url.config(
        default=_default_db,
        conn_max_age=600,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "frontend_dist",
]
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

WHITENOISE_ROOT = BASE_DIR / "frontend_dist"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]

CORS_ALLOW_ALL_ORIGINS = os.environ.get(
    "CORS_ALLOW_ALL_ORIGINS", "True" if ON_VERCEL else "False"
).lower() in (
    "1",
    "true",
    "yes",
)
