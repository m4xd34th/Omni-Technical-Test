"""
Django settings for technical_test project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

from .envtools import getenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv(
    "SECRET_KEY",
    default="django-insecure-p5*4tmq)*2h2x_!a$6mh+roqz7=#i1bs3j-z!g=(le5+t^=s44",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv("DEBUG", default=False, coalesce=bool)

ALLOWED_HOSTS = ["*"]

USE_X_FORWARDED_HOST = False
SESSION_COOKIE_HTTPONLY = True

SERVER_URL = os.getenv("SERVER_URL", default="*")


APPEND_SLASH = False

# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
]

LOCAL_APPS = [
    "store",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "technical_test.urls"

AUTH_USER_MODEL = "store.Client"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates", str(BASE_DIR.joinpath("templates"))],
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

WSGI_APPLICATION = "technical_test.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": getenv("POSTGRES_DEFAULT_DB", default="postgres"),
        "USER": getenv("POSTGRES_DEFAULT_USER", default="postgres"),
        "PASSWORD": getenv("POSTGRES_DEFAULT_PASSWORD", default="postgres"),
        "HOST": getenv("POSTGRES_DEFAULT_HOSTNAME", default="postgres"),
        "PORT": 5432,
        "CONN_MAX_AGE": 600,
        "DISABLE_SERVER_SIDE_CURSORS": True,
    },
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "../collected_static")
STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Django Rest Framework

REST_FRAMEWORK = {
    "PAGINATE_BY": 30,
    "PAGINATE_BY_PARAM": "per_page",
    "MAX_PAGINATE_BY": 1000,
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S%z",
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "store.authentication.BearerAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "commons.rest_framework.pagination.FullPageNumberPagination10",
}
if getenv("BROWSABLE_API_RENDERER", default=False, coalesce=bool):
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = REST_FRAMEWORK[
        "DEFAULT_RENDERER_CLASSES"
    ] + ["rest_framework.renderers.BrowsableAPIRenderer"]


# Django Login redirect

LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

# Email Configuration
EMAIL_PORT = 1025
EMAIL_HOST = 'localhost'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# CORS_REPLACE_HTTPS_REFERER      = True
# HOST_SCHEME                     = "https://"
# SECURE_PROXY_SSL_HEADER         = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT             = True
# SESSION_COOKIE_SECURE           = True
# CSRF_COOKIE_SECURE              = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
# SECURE_HSTS_SECONDS             = 1000000
# SECURE_FRAME_DENY               = True
# SECURE_REDIRECT_EXEMPT = ["actualizacion", "creacion", "normalizacion"]
