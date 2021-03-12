from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from decouple import config

SQLALCHEMY_DATABASE_URL = f"postgresql://{config('DB_USER', '')}:{config('DB_USER_PASSWORD')}@localhost:5432/{config('DB_NAME')}" # noqa

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
