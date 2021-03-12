from decouple import config


SECRET_KEY = config('SECRET_KEY', '')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7
