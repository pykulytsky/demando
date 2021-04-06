from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from base import settings


engine = create_engine(settings.TEST_DB_DSN)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
