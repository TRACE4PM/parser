from parser.main import parser
from parser.models.parameters import Parameters

file_path = "../data_example/res0.log"
collection = []
parameters = Parameters(
    parser_type="custom",
    parser_format='%h %l %u %t "%r" %>s %b "%{Referer}i" "%{User-Agent}i"',
)

print("test")

def test_parser():

    list_client = parser(
        file=file_path, collection=collection, parameters=parameters  # type: ignore
    )

    print(list_client)


test_parser()