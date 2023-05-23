# Import necessary modules
import re
from decimal import Decimal

from apachelogs import LogParser

from .models.client import Client_Model
from .models.parameters import Parameters, log_type
from .models.request import Request_Model
from .models.session import Session_Model


def line_is_valuable(temp: list, line: str):
    """Function to determine if a line from the log file is valuable

    Args:
        temp (list): list of keywords to exclude
        line (str): line to be processed

    Returns:
        bool: True if the line is valuable, False otherwise 
    """
    for i in temp:
        if i in line:
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


def replace_space_with_underscore(line):
    """Function to replace spaces with underscores in a string between two hashes

    Args:
        line (str): string to be processed

    Returns:
        str: processed string
    """
    pattern = r'(?<=##)[a-zA-Z ]+(?=[^#]*##)'
    return re.sub(pattern, lambda match: match.group().replace(' ', '_'), line)


def concatenate(unit: int, decimal: int) -> Decimal:
    """Function to concatenate two numbers

    Args:
        unit (int): unit part
        decimal (int): decimal part

    Returns:
        Decimal: concatenated number
    """
    return Decimal(str(unit) + '.' + str(decimal))


def get_unit_and_decimal(number: Decimal):
    """Function to get unit and decimals from a Decimal

    Args:
        number (Decimal): number to be split

    Returns:
        tuple[int, int]: unit and decimals
    """
    return int(str(number).split('.')[0]), int(str(number).split('.')[1])


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
        user_agent=str(entry.headers_in["User-Agent"])
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
    return Request_Model(
        request_id=concatenate(id_session, id_request),
        request_time=entry.request_time,
        request_url=str(entry.request_line),
        response_code=str(entry.final_status),
        referer=str(entry.headers_in["Referer"])
    )


async def compute(file, collection: list, parameters: Parameters):
    """Function to parse the log file

    Args:
        file (str): path of the log file
        collection (list): list of clients already existing
        parameters (Parameters): parameters of the parser

    Returns:
        list_client(list): list of clients parsed from the log file
    """
    # import parameters from Parameters Model
    parser_format = parameters.parser_format
    session_time_limit = parameters.session_time_limit
    exclude_keywords = parameters.exclude_keywords

    # Create a parser object
    parser = LogParser(parser_format, encoding="utf-8")

    # get the clients from the collection (if any)
    dict_client = {}
    for client in collection:
        dict_client[client.client_id] = client

    with open(file, "r") as f:
        for entry in f:
            # Replace spaces with underscores in the relevant portion of the line
            entry = replace_space_with_underscore(entry)
            # Check if the line is valuable
            if line_is_valuable(exclude_keywords, entry):
                entry = parser.parse(entry)

                client_id, country, city = get_id_contry_city(
                    entry.remote_host)
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
                    if (entry.request_time - last_req_time).total_seconds() < session_time_limit:
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
