import dj_database_url
import os
from pathlib import Path
import environ
from django.utils.translation import gettext_lazy as _

# Инициируем чтение .env
BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env(
    DEBUG=(bool, False)
)
env.read_env(BASE_DIR / '.env')

# Безопасность
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# Статика
STATIC_ROOT = os.path.join(BASE_DIR / 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = [BASE_DIR / "static"]

# Медиа
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rental',
]

# Мидлвары
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'config.urls'

# Шаблоны
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Пассворд-валидаторы
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Локализация
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGES = [
    ('en', _('English')),
    ('ru', _('Russian')),
]

# Где лежат ваши .po/.mo:
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]


# Email (по умолчанию SMTP через env)
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', default='')
EMAIL_PORT = env('EMAIL_PORT', default=587)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', True)
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='webmaster@localhost')
ADMIN_EMAIL = env('ADMIN_EMAIL', default=DEFAULT_FROM_EMAIL)

# Stripe ключи из env
STRIPE_PUBLIC_KEY = env('STRIPE_PUBLIC_KEY', default='')
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY', default='')


DATABASES = {
    'default': dj_database_url.config(conn_max_age=600
        #default=os.environ.get('DATABASE_URL_PROD'),
    )
}

# Доверенные источники для CSRF
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Безопасность
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Логи (пример простого консольного)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

