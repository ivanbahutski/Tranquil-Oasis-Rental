# settings_prod.py

import os
import environ
from pathlib import Path

# --- Настройки окружения ---
BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DEBUG=(bool, False)
)

# Читаем переменные из .env
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# --- Основные настройки ---
SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = ['yourdomain.com', '127.0.0.1', 'localhost']  # Укажи свой домен

# --- Приложения ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rental',  # твоё приложение
]

# --- Middleware ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# --- База данных ---
DATABASES = {
    'default': env.db(),  # автоматически подтянет из .env строку DATABASE_URL
}

# --- Статические файлы ---
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# --- Настройки электронной почты ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
ADMIN_EMAIL = env('ADMIN_EMAIL')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

# --- Stripe ---
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')
STRIPE_PUBLIC_KEY = env('STRIPE_PUBLIC_KEY')