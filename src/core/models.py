from datetime import datetime

from sqlalchemy import Column, DateTime

from .database import Base


class Timestamped(Base):
    __abstract__ = True
    created = Column(DateTime, default=datetime.now())
    updated = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
