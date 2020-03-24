from .settings import *

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'postgres',
    #     'USER': 'postgres',
    #     'PASSWORD': 'supersecretpassword',
    #     'HOST': 'db',
    #     'PORT': 5432,
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'ec2-174-129-252-255.compute-1.amazonaws.com',
        'NAME': 'd9ld4f06dr4urv',
        'USER': 'yoxuxgfzifyhwc',
        'PASSWORD': 'd033a8519fa2c26a7216faedd7247660b09df5f663803cd5e047cb19b0ebab8b',
        'PORT': 5432,
    }
}

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3006',
    'http://localhost:8081'
]