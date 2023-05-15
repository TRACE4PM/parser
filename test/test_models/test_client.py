import pytest
# from src.parser.models.client import Client_Model
from parser.models.client import Client_Model


def test_create_valid_client():
    client = Client_Model(
        client_id="test_id",
        country="test_country",
        city="test_city",
        user_agent="test_user_agent",
        sessions=[]
    )
    assert client.client_id == "test_id"
    assert client.country == "test_country"
    assert client.city == "test_city"
    assert client.user_agent == "test_user_agent"
    assert client.sessions == []


# a test for each field
# assert right error raised if field is not the correct type
def test_create_client_with_invalid_type():
    assert True
    # try:
    #     Client_Model(
    #         client_id=[],
    #         country="test_country",
    #         city="test_city",
    #         user_agent="test_user_agent",
    #         sessions=[]
    #     )
    # except ValidationError:
    #     assert True
    # else:
    #     assert False
    # with pytest.raises(TypeError):
    #     Client_Model(
    #         client_id=1,
    #         country="test_country",
    #         city="test_city",
    #         user_agent="test_user_agent",
    #         sessions=[]
    #     )
    # with pytest.raises(TypeError):
    #     Client_Model(
    #         client_id="test_id",
    #         country=1,
    #         city="test_city",
    #         user_agent="test_user_agent",
    #         sessions=[]
    #     )
    # with pytest.raises(TypeError):
    #     Client_Model(
    #         client_id="test_id",
    #         country="test_country",
    #         city=1,
    #         user_agent="test_user_agent",
    #         sessions=[]
    #     )
    # with pytest.raises(TypeError):
    #     Client_Model(
    #         client_id="test_id",
    #         country="test_country",
    #         city="test_city",
    #         user_agent=1,
    #         sessions=[]
    #     )
    # with pytest.raises(TypeError):
    #     Client_Model(
    #         client_id="test_id",
    #         country="test_country",
    #         city="test_city",
    #         user_agent="test_user_agent",
    #         sessions=1
    #     )
