from config.settings.base import *  # noqa

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# База данных (по умолчанию SQLite)
DATABASES = {
    'default': env.db(
        'DATABASE_URL_DEV',
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
    )
}

# Локальная база — SQLite по умолчанию, консольный бэкенд для почты
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Безопасность для dev
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
