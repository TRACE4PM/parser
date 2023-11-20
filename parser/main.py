import re
from datetime import datetime

# from apachelogs import LogParser
import apache_log_parser as LogParser
import pandas as pd

from .models.client import Client_Model
from .models.parameters import Parameters, log_type
from .models.csv_parameters import CsvParameters
from .models.request import Request_Model
from .models.session import Session_Model
from .utils import clean_file


def line_is_valuable(exclude_keywords: list, log: str):
    """Function to determine if a line from the log file is valuable

    Args:
        exclude_keywords: list of keywords to exclude
        log (str): line to be processed

    Returns:
        bool: True if the line is valuable, False otherwise 
    """

    for keyword in exclude_keywords:
        if keyword in log:
            return False
    return True


def get_id_contry_city(expression):
    """Function to extract the id, country, and city from a string in the format "##id##country##city##"

    Args:
        expression (str): string to be processed

    Raises:
        ValueError: if the expression is not in the expected format

    Returns:
        tuple: id, country, city
    """
    pattern = r'^##(\w+)##([\w-]+)##([\w-]+)##$'
    match = re.match(pattern, expression)
    if match:
        if match.group(2) != "null":
            country = match.group(2)
        else:
            country = "None"
        if match.group(3) != "null":
            city = match.group(3)
        else:
            city = "None"
        return match.group(1), country, city
    else:
        raise ValueError('Expression is not in the expected format.')


def concatenate(unit: int, decimal: int) -> str:
    """Function to concatenate two numbers

    Args:
        unit (int): unit part
        decimal (int): decimal part

    Returns:
        string: concatenated number
    """
    string = str(unit) + '.' + str(decimal)
    return string


def get_unit_and_decimal(number: str):
    """Function to get unit and decimals from a string

    Args:
        number (Decimal): number to be split

    Returns:
        tuple[int, int]: unit and decimals
    """
    return int(str(number).split('.')[0]), int(str(number).split('.')[1])


# TODO: Move code before in utils.py

def create_client(entry: str, client_id_temp: str, country_temp: str, city_temp: str) -> Client_Model:
    """Function to create a client object from a log entry

    Args:
        entry (str): log entry
        client_id_temp (str): client id
        country_temp (str): country
        city_temp (str): city

    Returns:
        Client_Model: _description_
    """
    return Client_Model(
        client_id=client_id_temp,
        country=country_temp,
        city=city_temp,
        user_agent=entry["request_header_user_agent"]
    )


# TODO: this is a workaround !!
def csv_create_client(client_id):
    return Client_Model(
        client_id=client_id,
        country="",
        city="",
        user_agent=""
    )


def create_session(id: int) -> Session_Model:
    """Function to create a session object from a log entry

    Args:
        id (int): id of the session

    Returns:
        Session_Model: session object
    """
    return Session_Model(
        session_id=id
    )


def create_request(entry: str, id_session: int, id_request: int) -> Request_Model:
    """Function to create a request object from a log entry

    Args:
        entry (str): log entry
        id_session (int): id of the session
        id_request (int): id of the request

    Returns:
        Request_Model: request object
    """
    if entry["request_header_referer"] == "-":
        entry["request_header_referer"] = None
    return Request_Model(
        request_id=concatenate(id_session, id_request),
        request_time=entry["time_received_tz_datetimeobj"],
        request_url=entry["request_url"],
        response_code=entry["status"],
        referer=entry["request_header_referer"]
    )


# The same functions as create_request but for csv files
def create_action(parameters: CsvParameters, date: str, action: str, id_session: int, id_action: int) -> Request_Model:
    """Function to create a request object from a log entry

    Args:
        action:
        date:
        parameters: CsvParameters
        row (str): log entry
        id_session (int): id of the session
        id_action (int): id of the request

    Returns:
        Request_Model: request object
    """

    # s = row[0] + ':00'
    # print(s)

    ts = datetime.strptime(date, parameters.timestamp_format)
    return Request_Model(
        request_id=concatenate(id_session, id_action),
        request_time=ts,
        request_url=action,
        response_code=None,
        referer=None
    )


async def parser(file, collection: list, parameters: Parameters) -> list[Client_Model]:
    """Function to parse the log file

    Args:
        file (str): path of the log file
        collection (list): list of clients already existing
        parameters (Parameters): parameters of the parser

    Returns:
        list_client(list): list of clients parsed from the log file
    """
    # Clean the file using utils
    await clean_file(file)

    # import parameters from Parameters Model
    session_time_limit = parameters.session_time_limit
    exclude_keywords = parameters.exclude_keywords

    # Create a parser object
    parse = LogParser.make_parser(parameters.parser_format)

    # get the clients from the collection (if any)
    dict_client = {}
    for client in collection:
        dict_client[client.client_id] = client

    with open(file, "r", encoding='utf-8') as f:
        for entry in f:
            # Check if the line is valuable
            if line_is_valuable(exclude_keywords, entry):
                # Parse the entry with apache-log-parser
                entry = parse(entry)

                client_id, country, city = get_id_contry_city(entry["remote_host"])
                # If the client is not in the dict, create it
                if client_id not in dict_client.keys():
                    # Create User
                    cli = create_client(
                        entry, client_id, country, city)

                    # Create session with id 1
                    session_id = int(1)
                    sess = create_session(session_id)

                    # Create request with id 1
                    request_id = int(1)
                    req = create_request(entry, session_id, request_id)

                    sess.requests.append(req)
                    cli.sessions.append(sess)
                    dict_client[client_id] = cli

                # Append the request to the client
                else:
                    cli = dict_client[client_id]
                    last_req_time = cli.sessions[-1].requests[-1].request_time
                    # If the request time is less than 1 hour from the previous request, add it to the same session
                    if (entry["time_received_tz_datetimeobj"] - last_req_time).total_seconds() < session_time_limit:
                        # Create request with id depending on the previous
                        session_id, request_id = get_unit_and_decimal(
                            cli.sessions[-1].requests[-1].request_id)
                        request_id += int(1)
                        req = create_request(entry, session_id, request_id)
                        # Add the request to the lastsession
                        cli.sessions[-1].requests.append(req)

                    # Else, create a new session and add the request to it
                    else:
                        # Create session with id depending on the last session id
                        session_id = cli.sessions[-1].session_id + int(1)
                        sess = create_session(session_id)

                        # Create request with id depending on the number of session id
                        request_id = int(1)
                        req = create_request(entry, session_id, request_id)

                        sess.requests.append(req)
                        cli.sessions.append(sess)
    # Add the all clients to the list
    list_client = []
    for val in dict_client.values():
        list_client.append(val.dict())
    return list_client


async def csv_parser(file, collection: list, parameters: CsvParameters) -> list[Client_Model]:
    # import parameters from Parameters Model
    session_time_limit = parameters.session_time_limit

    # get the clients from the collection (if any)
    dict_client = {}
    for client in collection:
        dict_client[client.client_id] = client

    # Read CSV file into DataFrame df
    # TODO: valider l'utilité de Pandas ?
    df = pd.read_csv(file, sep=parameters.separator)


    # Sorted because of Moodle DESC row order
    # TODO: As long as the date is a valid datetime, we must remove other date manipulations (create_action)

    # Create a new column with the timestamp in the right format
    # df[parameters.timestamp_column] = pd.to_datetime(df[parameters.timestamp_column], format=parameters.timestamp_format)
    df["parsed_ts"] = pd.to_datetime(df[parameters.timestamp_column], format=parameters.timestamp_format)
    # Sort the dataframe by timestamp
    df = df.sort_values(by="parsed_ts")


    # iterate over the dataframe

    for row in df.index:

        # get client id using session_id_column in current row
        client_id = df.loc[row, parameters.session_id_column]
        # df[parameters.session_id_column][row] # Could also be done using this line
        # print(client_id)
        # column_names = df.columns.values.tolist()
        # print(column_names)

        row_date = df.loc[row, parameters.timestamp_column]
        row_action = df.loc[row, parameters.action_column]

        # If the client is not in the dict, create it
        if client_id not in dict_client.keys():
            # Create User
            cli = csv_create_client(client_id)

            # Create session with id 1
            session_id = int(1)
            sess = create_session(session_id)

            # Create request with id 1
            request_id = int(1)

            # Create action

            action = create_action(parameters, row_date, row_action, session_id, request_id)

            sess.requests.append(action)
            cli.sessions.append(sess)
            dict_client[client_id] = cli

        # else add the request to the client
        else:
            cli = dict_client[client_id]
            last_req_time = cli.sessions[-1].requests[-1].request_time

            ts = datetime.strptime(row_date, parameters.timestamp_format)

            if (ts - last_req_time).total_seconds() < session_time_limit:
                # Create request with id depending on the previous
                session_id, request_id = get_unit_and_decimal(
                    cli.sessions[-1].requests[-1].request_id)
                request_id += int(1)
                action = create_action(parameters, row_date, row_action, session_id, request_id)
                # Add the request to the lastsession
                cli.sessions[-1].requests.append(action)
                # Else, create a new session and add the request to it
            else:
                # Create session with id depending on the last session id
                session_id = cli.sessions[-1].session_id + int(1)
                sess = create_session(session_id)

                # Create request with id depending on the number of session id
                request_id = int(1)
                action = create_action(parameters, row_date, row_action, session_id, request_id)

                sess.requests.append(action)
                cli.sessions.append(sess)

    # Add the all clients to the list
    list_client = []
    for val in dict_client.values():
        list_client.append(val.dict())
    return list_client

