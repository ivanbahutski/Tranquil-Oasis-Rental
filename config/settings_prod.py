from .base import *

DEBUG = False

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

DATABASES = { 'default': dj_database_url.parse(env('DATABASE_URL')) }

STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY') STRIPE_PUBLIC_KEY = env('STRIPE_PUBLIC_KEY')