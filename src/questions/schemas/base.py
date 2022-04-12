from datetime import datetime

from pydantic import BaseModel


class Timestamped(BaseModel):
    created: datetime
    updated: datetime
