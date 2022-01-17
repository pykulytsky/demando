from .database import Base
from sqlalchemy import Column, DateTime
from datetime import datetime


class Timestamped(Base):
    __abstract__ = True
    created = Column(DateTime, default=datetime.now())
    updated = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
