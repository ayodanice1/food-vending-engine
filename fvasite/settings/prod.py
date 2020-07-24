from fvasite.settings.base import *

import dj_database_url

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = [ '*' ]

db_from_env = dj_database_url.config(conn_max_age=500)

DATABASES['default'].update(db_from_env)

MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware',
]
