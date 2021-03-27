from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from gino.ext.starlette import Gino # noqa

from . import settings

from . import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_USER_PASSWORD}@{settings.DB_HOST}:5432/{settings.DB_NAME}" # noqa

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db = Gino(
    dsn=settings.DB_DSN,
    pool_min_size=settings.DB_POOL_MIN_SIZE,
    pool_max_size=settings.DB_POOL_MAX_SIZE,
    echo=settings.DB_ECHO,
    ssl=settings.DB_SSL,
    use_connection_for_request=settings.DB_USE_CONNECTION_FOR_REQUEST,
    retry_limit=settings.DB_RETRY_LIMIT,
    retry_interval=settings.DB_RETRY_INTERVAL,
)
