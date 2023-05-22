from .base import Base_model
from pydantic import validator


# List of standard log formats
log_type = {
    "custom": "",
    "Apache Common": "%h %l %u %t \"%r\" %>s %b",
    "Apache Combined": "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"",
    "Nginx default": "$remote_addr - $remote_user [$time_local] \"$request\" $status $body_bytes_sent \"$http_referer\" \"$http_user_agent\"",
    "AWS ELB access": "%t %h:%{X-Forwarded-For}i %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" %D",
    "Microsoft IIS": "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"",
    "JSON": "{\"remote_host\":\"%h\",\"remote_log_name\":\"%l\",\"remote_user\":\"%u\",\"request_time\":\"%t\",\"request_line\":\"%r\",\"final_status\":\"%>s\",\"bytes_sent\":\"%b\",\"headers_in\":{\"Referer\":\"%{Referer}i\",\"User-Agent\":\"%{User-Agent}i\"}}",
}


class Parameters(Base_model):
    parser_type: str
    parser_format: str = None
    session_time_limit: int = 3600
    exclude_keywords: list[str]

    @validator('parser_type, parser_format', always=True)
    def parser_type_and_parser_format_must_be_valid(cls, v, values):
        if v not in log_type.keys():
            raise ValueError(f"parser_type must be one of {log_type.keys()}")
        if v == "custom":
            assert values["parser_format"] != None, "parser_format must be set if parser_type is custom"
            assert values["parser_format"] == "", "parser_format must be set if parser_type is custom"
        if v != "custom":
            values["parser_format"] = log_type[v]
        return v, values

    @validator('session_time_limit', always=True)
    def session_time_limit_must_be_positive(cls, session_time_limit):
        assert session_time_limit > 0, "session_time_limit must be positive"
        return session_time_limit
