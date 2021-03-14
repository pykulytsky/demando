from decouple import config


SECRET_KEY = config('SECRET_KEY', '')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

DB_NAME = config('DB_NAME', 'demando')
TEST_DB_NAME = config('TEST_DB_NAME', 'demando')
DB_USER = config('DB_USER', 'demando')
DB_USER_PASSWORD = config('DB_USER_PASSWORD', '1234')
DB_HOST = config('DB_HOST', 'db')
