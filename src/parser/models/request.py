from .base import Base_model
from datetime import datetime


class Request_Model(Base_model):
    request_id: str
    request_time: datetime | None = None
    request_url: str | None = None
    response_code: str | None = None
    referer: str | None = None
