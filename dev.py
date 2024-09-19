import json

from parser.main import parser
from parser.main import csv_parser
from parser.models.parameters import Parameters
from parser.models.csv_parameters import CsvParameters

file_path = "test/test_files/cluster_log_0.csv"
collection = []

# parameters = Parameters(
#     parser_type="custom",  # TODO: Rename to -> log_type
#     parser_format='%h %l %u %t "%r" %>s %b "%{Referer}i" "%{User-Agent}i"',
# )

parameters = CsvParameters(
    separator=";",
    timestamp_column="timestamp",
    timestamp_format="%Y-%m-%d %H:%M:%S",
    action_column="action",
    session_id_column="client_id",
    session_time_limit=3600
)

print(parameters)


def test_parser():
    list_client = csv_parser(
        file=file_path, collection=collection, parameters=parameters  # type: ignore
    )

    # print(list_client)
    # serialize list_client in JSON
    print(json.dumps(list_client, indent=4, sort_keys=True, default=str))


test_parser()
