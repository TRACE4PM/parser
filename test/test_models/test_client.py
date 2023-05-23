from parser.models.client import Client_Model

import pytest


def test_create_valid_client():
    client = Client_Model(
        client_id="test_id",
    )
    assert client.client_id == "test_id"
    assert client.country == None
    assert client.city == None
    assert client.user_agent == None
    assert client.sessions == []


# create a client with an invalid client_id
def test_create_invalid_client_id():
    with pytest.raises(ValueError):
        Client_Model(
            client_id=[],
            country="test_country",
            city="test_city",
            user_agent="test_user_agent",
            sessions=[]
        )


# create a client with an invalid sessions list
def test_create_invalid_sessions():
    with pytest.raises(ValueError):
        Client_Model(
            client_id="test_id",
            country="test_country",
            city="test_city",
            user_agent="test_user_agent",
            sessions="test_sessions"
        )
