from pydantic import validator, root_validator

from .base import Base_model


# List of standard log formats
log_type = {
    "custom": "",
    "Apache Common":  "%h %l %u %t \"%r\" %>s %b",
    "Apache Combined": "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"",
    "Nginx default": "$remote_addr - $remote_user [$time_local] \"$request\" $status $body_bytes_sent \"$http_referer\" \"$http_user_agent\"",
    "AWS ELB access": "%t %h:%{X-Forwarded-For}i %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" %D",
    "Microsoft IIS": "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"",
    "JSON": "{\"remote_host\":\"%h\",\"remote_log_name\":\"%l\",\"remote_user\":\"%u\",\"request_time\":\"%t\",\"request_line\":\"%r\",\"final_status\":\"%>s\",\"bytes_sent\":\"%b\",\"headers_in\":{\"Referer\":\"%{Referer}i\",\"User-Agent\":\"%{User-Agent}i\"}}",
}


class Parameters(Base_model):
    """Parameters model for the parser

    Args:
        parser_type (log_type): log standard format
        parser_format (str, optional): custom log format. Defaults to None.
        session_time_limit (int, optional): session time limit in seconds. Defaults to 3600.
        exclude_keywords (list[str], optional): list of keywords to exclude from the log file. Defaults to [].

    Raises:
        ValueError: parser type must be in log_type
        ValueError: parser_format must be set when parser_type is 'custom'
        ValueError: parser_format must be null when parser_type is not 'custom'
    """
    parser_type: str
    parser_format: str | None = None
    session_time_limit: int = 3600
    exclude_keywords: list[str] = []

    @root_validator
    def validate_parser_format(cls, values):
        parser_type = values.get('parser_type')
        parser_format = values.get('parser_format')

        if parser_type not in log_type:
            raise ValueError(f"Invalid parser_type: {parser_type}")
        if parser_type == "custom" and not parser_format:
            raise ValueError(
                "parser_format must be set when parser_type is 'custom'")
        if parser_type != "custom" and parser_format is not None:
            raise ValueError(
                "parser_format must be null when parser_type is not 'custom'")
        if parser_type != "custom":
            values['parser_format'] = log_type[parser_type]
        return values

    @validator('session_time_limit', always=True)
    def session_time_limit_must_be_positive(cls, session_time_limit):
        assert session_time_limit > 0, "session_time_limit must be positive"
        return session_time_limit

    # Assert that exclude_keywords is a list of strings
    @validator('exclude_keywords', always=True)
    def exclude_keywords_must_be_list_of_strings(cls, exclude_keywords):
        assert isinstance(exclude_keywords,
                          list), "exclude_keywords must be a list"
        for keyword in exclude_keywords:
            assert isinstance(
                keyword, str), "exclude_keywords must be a list of strings"
        return exclude_keywords
