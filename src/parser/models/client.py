from .base import Base_model
from .session import Session_Model


class Client_Model(Base_model):
    client_id: str
    country: str = None
    city: str = None
    user_agent: str = None
    sessions: list[Session_Model] = []
