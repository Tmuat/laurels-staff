"""
Base settings to build other settings files upon.
"""

import os
import environ
import logging

from pathlib import Path

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ------------------------------------------------------------------------------
# DJANGO ENV SETTINGS
# ------------------------------------------------------------------------------

# Settings for Django-environ
# https://django-environ.readthedocs.io/en/latest/#
env = environ.Env()

# Reading .env file
environ.Env.read_env()

# ------------------------------------------------------------------------------
# GENERAL
# ------------------------------------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY")

# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)

# https://docs.djangoproject.com/en/3.1/topics/settings/
DJANGO_SETTINGS_MODULE_ENV = env("DJANGO_SETTINGS_MODULE_ENV")

# https://docs.djangoproject.com/en/3.1/ref/contrib/messages/
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = "GB"

# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-GB"

# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [str(BASE_DIR / "locale")]

# https://docs.djangoproject.com/en/3.2/releases/3.2/#customizing-type-of-auto-created-primary-keys
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ------------------------------------------------------------------------------
# URLS
# ------------------------------------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "laurels.urls"

# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "laurels.wsgi.application"

# ------------------------------------------------------------------------------
# APPS
# ------------------------------------------------------------------------------

DJANGO_APPS = [
    "django_admin_env_notice",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.humanize",
    "django.forms",
]

THIRD_PARTY_APPS = [
    "admin_honeypot",
    "crispy_forms",
    "django_otp",
    "django_otp.plugins.otp_static",
    "django_otp.plugins.otp_totp",
    "two_factor",
    "mathfilters",
]

LOCAL_APPS = [
    "users",
    "invitations",
    "regionandhub",
    "home",
    "accounts",
    "properties",
    "stats",
    "lettings",
    "weekends",
    "boards",
    "touts",
]

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

# ------------------------------------------------------------------------------
# AUTHENTICATION
# ------------------------------------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.CustomUser"

# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "/"

# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "accounts:login"

# https://docs.djangoproject.com/en/dev/ref/settings/#logout-redirect-url
LOGOUT_REDIRECT_URL = "/"

# ------------------------------------------------------------------------------
# MIDDLEWARE
# ------------------------------------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ------------------------------------------------------------------------------
# PASSWORDS
# ------------------------------------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa
        "OPTIONS": {
            "min_length": 12,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"  # noqa
    },
]

# ------------------------------------------------------------------------------
# TEMPLATES
# ------------------------------------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.tz",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django_admin_env_notice.context_processors.from_settings",
                "laurels.context_processors.active_hubs",
            ],
            "builtins": [
                "crispy_forms.templatetags.crispy_forms_tags",
                "crispy_forms.templatetags.crispy_forms_field",
            ],
        },
    }
]

# ------------------------------------------------------------------------------
# SECURITY
# ------------------------------------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True

# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True

# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True

# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# ------------------------------------------------------------------------------
# ADMIN
# ------------------------------------------------------------------------------

# Django Admin URL.
ADMIN_URL = env("DJANGO_ADMIN_URL")

# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [(env.str("DJANGO_ADMIN_NAME"), env.str("DJANGO_ADMIN_EMAIL"))]

# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# ------------------------------------------------------------------------------
# STATIC
# ------------------------------------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)  # noqa

# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # noqa

# ------------------------------------------------------------------------------
# MEDIA
# ------------------------------------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = os.path.join(BASE_DIR, "media")  # noqa


# ------------------------------------------------------------------------------
# crispy-forms
# ------------------------------------------------------------------------------
# https://django-crispy-forms.readthedocs.io/en/latest/index.html

CRISPY_TEMPLATE_PACK = "bootstrap4"

# ------------------------------------------------------------------------------
# GET-ADDRESS
# ------------------------------------------------------------------------------
# https://getaddress.io/Documentation

GET_ADDRESS_KEY = env("GET_ADDRESS_API_KEY")


# ------------------------------------------------------------------------------
# EMAILS
# ------------------------------------------------------------------------------

NO_REPLY_EMAIL = env("NO_REPLY_EMAIL")
ADMIN_EMAIL = env("ADMIN_EMAIL")

# ------------------------------------------------------------------------------
# BOARDS
# ------------------------------------------------------------------------------
# http://signmaster.agencyexpress.net/api/v1/api-docs.pdf

BOARDS_URL = env("BOARDS_URL")
BOARDS_API_KEY = env("BOARDS_API_KEY")
BOARDS_COMPANY_KEY = env("BOARDS_COMPANY_KEY")
