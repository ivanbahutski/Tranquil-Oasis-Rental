from .base import *

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY', default='test_secret_key')
STRIPE_PUBLIC_KEY = env('STRIPE_PUBLIC_KEY', default='test_public_key')

# Отключаем переадресацию на HTTPS для локальной разработки
SECURE_SSL_REDIRECT = False

# Чтобы не требовать куки с флагом secure
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Чтобы получать более подробные ошибки на локали
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
