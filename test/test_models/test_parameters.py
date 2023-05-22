from pydantic import ValidationError, validator
import pytest
from parser.models.parameters import Parameters, log_type


def test_valid_parameters():
    """
    Test if the parser_format is well attribued from the dict
    """
    parameters = Parameters(
        parser_type="Apache Common",
        session_time_limit=15,
        exclude_keywords=["test1", "test2"]
    )
    assert parameters.parser_type == "Apache Common"
    # assert parameters.parser_format == log_type["Apache Common"]
    assert parameters.session_time_limit == 15
    assert parameters.exclude_keywords == ["test1", "test2"]


# def test_parameters_invalid_type():
#     """
#     Test if the parser_type is in the dict of standard log formats
#     """
#     with pytest.raises(ValidationError) as e:
#         Parameters(
#             parser_type="test",
#             session_time_limit=15,
#             exclude_keywords=["test1", "test2"]
#         )
#     assert e.value.errors() == [{
#         'loc': ('parser_type',),
#         'msg': 'parser_type must be one of dict_keys([\'custom\', \'Apache Common\', \'Apache Combined\', \'Nginx default\', \'AWS ELB access\', \'Microsoft IIS\', \'JSON\'])',
#         'type': 'value_error'
#     }]


# def test_parameters_empty_format():
#     """
#     Test if the parser_format is specified if parser type is "custom"
#     """
#     with pytest.raises(ValidationError) as e:
#         Parameters(
#             parser_type="custom",
#             session_time_limit=15,
#             exclude_keywords=["test1", "test2"]
#         )
#     assert e.value.errors() == [{
#         'loc': ('parser_format',),
#         'msg': 'Parser format must be specified if parser type is "custom".',
#         'type': 'value_error'
#     }]


# def test_parameters_negative_time_limit():
#     """
#     Test if the session_time_limit is positive
#     """
#     with pytest.raises(ValidationError) as e:
#         Parameters(
#             parser_type="Apache Common",
#             session_time_limit=-15,
#             exclude_keywords=["test1", "test2"]
#         )
#     assert e.value.errors() == [{
#         'loc': ('session_time_limit',),
#         'msg': 'session_time_limit must be positive',
#         'type': 'assertion_error',
#     }]


# def test_parameters_invalid_exclude_keywords():
#     # Test if the exclude_keywords is a list of strings
#     with pytest.raises(ValidationError) as e:
#         Parameters(
#             parser_type="Apache",
#             session_time_limit=15,
#             exclude_keywords=["test1", 2]
#         )
#     assert e.value.errors() == [{
#         'loc': ('exclude_keywords', 1),
#         'msg': 'str type expected',
#         'type': 'type_error.str'
#     }]

# def test_valid_apache_parameters():
#     """
#     Test if the parser_format is well attribued from the dict
#     """
#     parameters = Parameters(
#         parser_type="Apache",
#         session_time_limit=15,
#         exclude_keywords=["test1", "test2"]
#     )
#     assert parameters.parser_type == "Apache"
#     assert parameters.parser_format == log_type["Apache"]
#     assert parameters.session_time_limit == 15
#     assert parameters.exclude_keywords == ["test1", "test2"]
