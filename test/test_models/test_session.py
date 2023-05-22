from pydantic import ValidationError
from parser.models.session import Session_Model, Request_Model


def test_valid_session_model_without_requests():
    # Create a valid Session_Model instance without requests
    session = Session_Model(
        session_id=1
    )
    # Validate the model attributes
    assert session.session_id == 1
    assert session.requests == []


def test_valid_session_model_with_invalid_requests():
    # Create a valid Session_Model instance with invalid requests
    try:
        session = Session_Model(
            session_id=1,
            requests=[1, 2, 3]
        )
    except ValidationError as e:
        assert e.errors() == [
            {
                'loc': ('requests', 0),
                'msg': 'value is not a valid dict',
                'type': 'type_error.dict'
            },
            {
                'loc': ('requests', 1),
                'msg': 'value is not a valid dict',
                'type': 'type_error.dict'
            },
            {
                'loc': ('requests', 2),
                'msg': 'value is not a valid dict',
                'type': 'type_error.dict'
            }
        ]


def test_valid_session_model_with_requests():
    # Create a valid Session_Model instance with valid requests
    request = Request_Model(
        request_id=1,
        request_time="2023-05-15T14:30:00",
        request_url="http://example.com",
        response_code="200",
        referer="http://referrer.com"
    )
    session = Session_Model(
        session_id=1,
        requests=[request.dict()]
    )
    assert session.session_id == 1
    assert session.requests == [request.dict()]


def test_invalid_session_model():
    # Create an invalid Session_Model instance and check the validation error
    try:
        invalid_session = Session_Model(
            session_id="Not an int",
            requests="Not a list"
        )
    except ValidationError as e:
        assert e.errors() == [
            {
                'loc': ('session_id',),
                'msg': 'value is not a valid integer',
                'type': 'type_error.integer'
            },
            {
                'loc': ('requests',),
                'msg': 'value is not a valid list',
                'type': 'type_error.list'
            }
        ]
