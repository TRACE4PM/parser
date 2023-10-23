from pydantic import validator, root_validator

from .base import Base_model


class CsvParameters(Base_model):
    """Parameters model for the CSV parser

    Args:
        session_time_limit (int, optional): session time limit in seconds. Defaults to 3600.
        exclude_keywords (list[str], optional): list of keywords to exclude from the log file. Defaults to [].

    Raises:
        ValueError: timestamp_column must be set
        # ValueError: parser_format must be set when parser_type is 'custom'
        # ValueError: parser_format must be null when parser_type is not 'custom'
    """

    separator: str = ","
    timestamp_column: str  # | None = None
    timestamp_format: str
    action_column: str
    session_id_column: str
    session_time_limit: int = 3600
    exclude_keywords: list[str] = []  # Could be used to exclude some lines from the log file

    @root_validator
    def validate_parser_format(cls, values):
        # timestamp_column = values.get('timestamp_column')
        #
        # # parser_type = values.get('parser_type')
        # # parser_format = values.get('parser_format')
        # #
        #
        # if timestamp_column is None:
        #     raise ValueError(
        #         "timestamp_column must be set")

        return values

        # if parser_type not in log_type:
        #     raise ValueError(f"Invalid parser_type: {parser_type}")
        # if parser_type == "custom" and not parser_format:
        #     raise ValueError(
        #         "parser_format must be set when parser_type is 'custom'")
        # if parser_type != "custom" and parser_format is not None:
        #     raise ValueError(
        #         "parser_format must be null when parser_type is not 'custom'")
        # if parser_type != "custom":
        #     values['parser_format'] = log_type[parser_type]
        # return values

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
