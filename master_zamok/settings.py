from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env from project root
load_dotenv(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
DEBUG = os.getenv("DEBUG", "True") == "True"


ALLOWED_HOSTS = ['.masterzamok.pro','31.31.196.78','www.masterzamok.pro','185.221.153.228', 'localhost', '127.0.0.1', '91.201.40.138']

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "mainapp",
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

ROOT_URLCONF = "master_zamok.urls"

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
                "mainapp.context_processors.contact_info",  # Контактная информация
            ],
        },
    },
]

WSGI_APPLICATION = "master_zamok.wsgi.application"

# Database
# --------------------------------
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")

# Convert string to Django DB config
if DATABASE_URL.startswith("sqlite:///"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / DATABASE_URL.replace("sqlite:///", ""),
        }
    }
else:
    # PostgreSQL or others (not used now, but left for future)
    import dj_database_url
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL)}


# Password validation
# --------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
# Для production: директория, куда collectstatic собирает все статические файлы
STATIC_ROOT = BASE_DIR / "staticfiles"
# Директории, откуда собирать статические файлы (только если директория существует)
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Закомментируйте SMTP настройки и используйте консольный бэкенд
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ============================================================================
# НАСТРОЙКИ EMAIL
# ============================================================================
# ВНИМАНИЕ: Основные настройки email теперь управляются через админ-панель
# (модель EmailSettings). Эти настройки используются только как fallback
# для системных уведомлений Django и при первой инициализации БД.
# 
# Для изменения настроек email перейдите в админ-панель:
# /admin/mainapp/emailsettings/1/change/
# ============================================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_TIMEOUT = 10  # Таймаут подключения к SMTP серверу (секунды)

# Email адрес для отправки (можно переопределить через .env)
# Используется только для системных уведомлений Django
EMAIL_FROM = os.getenv("EMAIL_FROM", "schkurko.egor@yandex.ru")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "sjaxfyvovyrngury")
EMAIL_FROM_NAME = os.getenv("EMAIL_FROM_NAME", "MasterZamok")  # Имя отправителя в письмах

# Настройки SMTP (используем одну переменную для упрощения)
EMAIL_HOST_USER = EMAIL_FROM
EMAIL_HOST_PASSWORD = EMAIL_PASSWORD
# Формат: "Имя <email>" - в почтовых клиентах будет отображаться "MasterZamok"
DEFAULT_FROM_EMAIL = f"{EMAIL_FROM_NAME} <{EMAIL_FROM}>"  # Адрес отправителя для всех писем
SERVER_EMAIL = EMAIL_FROM  # Адрес для системных уведомлений Django (без имени, только email)

# Адреса для получения уведомлений о новых отзывах (можно указать несколько через запятую)
# Используются только как fallback, основная конфигурация в БД (EmailSettings)
REVIEW_NOTIFICATION_EMAIL_STR = os.getenv("REVIEW_NOTIFICATION_EMAIL", "allianzufa@gmail.com,schkurko.egor@yandex.ru")
# Преобразуем строку в список адресов
REVIEW_NOTIFICATION_EMAIL = [email.strip() for email in REVIEW_NOTIFICATION_EMAIL_STR.split(',') if email.strip()]

# Адреса для получения уведомлений о новых заявках/заказах (можно указать несколько через запятую)
# Используются только как fallback, основная конфигурация в БД (EmailSettings)
ORDER_NOTIFICATION_EMAIL_STR = os.getenv("ORDER_NOTIFICATION_EMAIL", "allianzufa@gmail.com,schkurko.egor@yandex.ru")
# Преобразуем строку в список адресов
ORDER_NOTIFICATION_EMAIL = [email.strip() for email in ORDER_NOTIFICATION_EMAIL_STR.split(',') if email.strip()]

# Контактная информация
CONTACT_PHONE = os.getenv("CONTACT_PHONE", "+7 (993) 962-50-87")
CONTACT_PHONE_TEL = os.getenv("CONTACT_PHONE_TEL", "+79939625087")  # Формат для tel: ссылок (без пробелов и скобок)

# Настройки логирования
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'django.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'mainapp': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}