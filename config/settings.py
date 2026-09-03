import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env if present
load_dotenv(BASE_DIR / ".env")

# SECURITY
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-tourist-safety-system-key-change-in-prod")
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# INSTALLED APPS
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "apps.users",
    "apps.incidents",
    "apps.monitoring",
]

# MIDDLEWARE
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
]

# Safely include WhiteNoise middleware if installed
try:
    import whitenoise
    MIDDLEWARE.append("whitenoise.middleware.WhiteNoiseMiddleware")
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
except ImportError:
    pass

MIDDLEWARE.extend([
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
])

ROOT_URLCONF = "config.urls"

# TEMPLATES
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "config.wsgi.application"

# DATABASE CONFIGURATION
# Supports DATABASE_URL (e.g. Render/PostgreSQL/MySQL), MS SQL Server (if USE_SQL_SERVER=True), or SQLite default
DATABASE_URL = os.getenv("DATABASE_URL")
USE_SQL_SERVER = os.getenv("USE_SQL_SERVER", "False").lower() in ("true", "1", "t")

if DATABASE_URL:
    try:
        import dj_database_url
        DATABASES = {
            "default": dj_database_url.config(
                default=DATABASE_URL,
                conn_max_age=600,
                conn_health_checks=True,
            )
        }
    except ImportError:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            }
        }
elif USE_SQL_SERVER:
    DATABASES = {
        "default": {
            "ENGINE": "mssql",
            "NAME": os.getenv("DB_NAME", "tourist_safety_db"),
            "HOST": os.getenv("DB_HOST", "localhost"),
            "PORT": os.getenv("DB_PORT", ""),
            "OPTIONS": {
                "driver": os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server"),
                "trusted_connection": "yes",
            },
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# INTERNATIONALIZATION
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# STATIC FILES
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static"
]
STATIC_ROOT = BASE_DIR / "staticfiles"

# DEFAULT PRIMARY KEY
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"