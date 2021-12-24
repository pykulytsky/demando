from starlette.config import Config
from sqlalchemy.engine.url import URL, make_url

from starlette.datastructures import Secret, URLPath


config = Config('settings.ini')

DEBUG = config('DEBUG', cast=bool, default=True)


SECRET_KEY = config('SECRET_KEY', default='')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

DB_DRIVER = config("DB_DRIVER", default="postgresql")
DB_NAME = config('DB_NAME', default='demando')
TEST_DB_NAME = config('TEST_DB_NAME', default='demando')
DB_USER = config('DB_USER', default='demando')
DB_USER_PASSWORD = config('DB_USER_PASSWORD', cast=Secret, default='1234')
DB_HOST = config('DB_HOST', cast=str, default='db')
DB_PORT = config('DB_PORT', cast=int, default='5432')

DB_DSN = config(
    'DB_DSN',
    cast=make_url,
    default=URL(
        drivername=DB_DRIVER,
        username=DB_USER,
        password=DB_USER_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
    )
)

TEST_DB_DSN = config(
    'TEST_DB_DSN',
    cast=make_url,
    default=URL(
        drivername=DB_DRIVER,
        username=DB_USER,
        password=DB_USER_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=TEST_DB_NAME,
    )
)

SENTRY_DSN = config(
    'SENTRY_DSN',
    default='https://e08875a22d804df08150988c6886b871@o504286.ingest.sentry.io/5673787'
)

SENDGRID_BASE_URL = config('SENDGRID_BASE_URL', cast=URLPath, default='')
SENDGRID_API_KEY = config('SENDGRID_API_KEY', cast=str, default='')
SENDGRID_VERIFY_EMAIL_TEMPLATE_ID = config('SENDGRID_VERIFY_EMAIL_TEMPLATE_ID', cast=str, default='')

EMAIL_HOST_USER = config('EMAIL_HOST_USER', cast=str, default='demando@info.com')
EMAIL_HOST_USER_NAME = config('EMAIL_HOST_USER_NAME', cast=str, default='Ivan Ivanov')
