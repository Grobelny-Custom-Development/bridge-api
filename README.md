# bridge-api


# V1 Heroku configuration
Configured STATIC_ROOT in settings
Configured Procfile
Added gunicorn to requirements
Added bridge-api-dev.herokuapp.com to ALLOWED_HOSTS
Added 'whitenoise.middleware.WhiteNoiseMiddleware' to middlewares for static asset management

Configure dj_database_url to pull in Heroku's Postgres db they built
