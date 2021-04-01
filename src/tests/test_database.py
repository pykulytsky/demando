from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from base import settings


SQLALCHEMY_DATABASE_URL = settings.TEST_DB_DSN

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
