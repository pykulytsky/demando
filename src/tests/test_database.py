from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from base import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_USER_PASSWORD}@{settings.DB_HOST}:5432/{settings.TEST_DB_NAME}" # noqa

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
