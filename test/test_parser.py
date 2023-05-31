import pytest
from parser.main import parser
from parser.models.parameters import Parameters
from decimal import Decimal
from datetime import datetime, timezone, timedelta


@pytest.mark.asyncio
async def test_compute_for_gallica():
    """Test the compute function with a Gallica log file
    """
    file = "test/test_files/Gallica.log"
    parameters = Parameters(
        parser_type="custom", parser_format="%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"")
    list_client = await parser(file, [], parameters)
    assert list_client == [{
        "client_id": "5205482e2f69631635db3e6ce0200f97",
        "country": "France",
        "city": "Châtillon",
        "user_agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "sessions": [{
            "session_id": 1,
            "requests": [{
                "request_id": str("1.1"),
                "request_time": datetime(2017, 3, 31, 10, 7, 24, tzinfo=timezone(timedelta(hours=2))),
                "request_url": "/rapport.html",
                "response_code": "200",
                "referer": None,
            }]
        }]
    }]
