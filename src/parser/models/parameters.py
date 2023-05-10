from .base import Base_model


class Parameters(Base_model):
    parser_type: str
    parser_format: str | None = None
    session_time_limit: int
    exclude_keywords: list[str]
