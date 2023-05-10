from .base import Base_model
from .session import Session_Model


class Client_Model(Base_model):
    client_id: str | None = None
    country: str | None = None
    city: str | None = None
    user_agent: str | None = None
    sessions: list[Session_Model] = []
