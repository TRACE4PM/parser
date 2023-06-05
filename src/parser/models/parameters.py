from pydantic import validator, root_validator
import json
from .base import Base_model

# List of standard log formats
log_type = json.load(
    open(file="src/parser/log_format.json")
)


class Parameters(Base_model):
    """Parameters model for the parser

    Args:
        parser_type (log_type): log standard format. Refer to log_format.json for the list of standard formats.
        parser_format (str, optional): custom log format. Defaults to None. Prefer to use parser_type instead.
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
