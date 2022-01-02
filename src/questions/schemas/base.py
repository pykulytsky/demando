from pydantic import BaseModel
from datetime import datetime


class Timestamped(BaseModel):
    created: datetime
    updated: datetime
