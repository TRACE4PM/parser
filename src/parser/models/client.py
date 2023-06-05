from .base import Base_model
from .session import Session_Model


class Client_Base_Model(Base_model):
    client_id: str
    country: str = None
    city: str = None
    user_agent: str = None


class Client_Model(Client_Base_Model):
    sessions: list[Session_Model] = []


class Client_Get_Model(Client_Base_Model):
    class Config:
        schema_extra = {
            "example": {
                "client_id": "self.client_id",
                "country": "self.country",
                "city": "self.city",
                "user_agent": "self.user_agent",
            }
        }
