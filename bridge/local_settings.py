from .settings import *

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'supersecretpassword',
        'HOST': 'db',
        'PORT': 5432,
    }
}

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3006',
    'http://localhost:8081'
]