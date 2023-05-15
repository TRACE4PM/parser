from .base import Base_model
from datetime import datetime
from decimal import Decimal


class Request_Model(Base_model):
    request_id: Decimal | None = None
    request_time: datetime | None = None
    request_url: str | None = None
    response_code: str | None = None
    referer: str | None = None
