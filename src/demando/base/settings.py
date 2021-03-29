from sqlalchemy.engine.url import URL, make_url
from starlette.config import Config
from starlette.datastructures import Secret


config = Config("settings.ini")


SECRET_KEY = config('SECRET_KEY', default='')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

DB_NAME = config('DB_NAME', default='demando')
TEST_DB_NAME = config('TEST_DB_NAME', default='demando')
DB_USER = config('DB_USER', default='demando')
DB_USER_PASSWORD = config('DB_USER_PASSWORD', default='1234')
DB_HOST = config('DB_HOST', default='db')

DEBUG = True

SENTRY_DSN = config(
    'SENTRY_DSN',
    default='https://e08875a22d804df08150988c6886b871@o504286.ingest.sentry.io/5673787'
)

TESTING = config("TESTING", cast=bool, default=False)

DB_DRIVER = config("DB_DRIVER", default="postgresql")
DB_HOST = config("DB_HOST", default='localhost')
DB_PORT = config("DB_PORT", cast=int, default=5432)
DB_USER = config("DB_USER", default=None)
DB_PASSWORD = config("DB_USER_PASSWORD", cast=Secret, default=None)
DB_DATABASE = config("DB_NAME", default=None)
DB_DSN = config(
    "DB_DSN",
    cast=make_url,
    default=URL(
        drivername=DB_DRIVER,
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_DATABASE,
    ),
)
DB_POOL_MIN_SIZE = config("DB_POOL_MIN_SIZE", cast=int, default=1)
DB_POOL_MAX_SIZE = config("DB_POOL_MAX_SIZE", cast=int, default=16)
DB_ECHO = config("DB_ECHO", cast=bool, default=False)
DB_SSL = config("DB_SSL", default=None)
DB_USE_CONNECTION_FOR_REQUEST = config(
    "DB_USE_CONNECTION_FOR_REQUEST", cast=bool, default=True
)
DB_RETRY_LIMIT = config("DB_RETRY_LIMIT", cast=int, default=1)
DB_RETRY_INTERVAL = config("DB_RETRY_INTERVAL", cast=int, default=1)

TESTING = config("TESTING", cast=bool, default=False)

if TESTING:
    if DB_DATABASE:
        DB_DATABASE += "_test"
    else:
        DB_DATABASE = "demando_test"
