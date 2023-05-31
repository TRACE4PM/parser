from datetime import datetime
from pydantic import ValidationError
from parser.models.request import Request_Model


def test_request_model():
    # Create a valid Request_Model instance
    request = Request_Model(
        request_id=str("1.23"),
        request_time="2023-05-15T14:30:00",
        request_url="http://example.com",
        response_code="200",
        referer="http://referrer.com"
    )

    # Validate the model attributes
    assert request.request_id == str("1.23")
    assert request.request_time == datetime(2023, 5, 15, 14, 30, 0)
    assert request.request_url == "http://example.com"
    assert request.response_code == "200"
    assert request.referer == "http://referrer.com"


def test_invalid_request_model():
    # Create an invalid Request_Model instance and check the validation error
    try:
        invalid_request = Request_Model(
            request_id=[],
            request_time="Not a datetime",
            request_url=[],
            response_code=[],
            referer=[]
        )
    except ValidationError as e:
        assert e.errors() == [
            {
                'loc': ('request_id',),
                'msg': 'str type expected',
                'type': 'type_error.str'
            },
            {
                'loc': ('request_time',),
                'msg': 'invalid datetime format',
                'type': 'value_error.datetime'
            },
            {
                'loc': ('request_url',),
                'msg': 'str type expected',
                'type': 'type_error.str'
            },
            {
                'loc': ('response_code',),
                'msg': 'str type expected',
                'type': 'type_error.str'
            },
            {
                'loc': ('referer',),
                'msg': 'str type expected',
                'type': 'type_error.str'
            }
        ]
