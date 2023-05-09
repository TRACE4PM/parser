# Import necessary modules
import io
import json
import re
from decimal import Decimal

from src.apachelogs import LogParser
from src.models.client import Client_Model
from src.models.request import Request_Model
from src.models.session import Session_Model

# Initialize the log parser with the format of the Apache log files
# parser = LogParser("%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"")

# List of strings that indicate non-valuable lines
# temp = []
# temp = ["/img", "/css", "/js", "/fontes","/browser_components", ".js", ".css", "/nom"]


# Function to read the json parameters file
def load_json_parameters():
    with open("src/json/parameter.json", "r") as f:
        j = json.load(f)
        exclude_keywords = j["exclude_keywords"]
        session_time_limit = j["session_time_limit"]
        parser_type = j["parser_type"]
        parser_format = j["parser_format"]
        return parser_type, parser_format, session_time_limit, exclude_keywords,


# Function to determine if a line from the log file is valuable
def line_is_valuable(temp, line):
    for i in temp:
        if i in line:
            return False
    return True


# Function to extract the id, country, and city from a string in the format "##id##country##city##"
def get_id_contry_city(expression):
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


# Function to replace spaces with underscores in a string between "##" markers
def replace_space_with_underscore(line):
    pattern = r'(?<=##)[a-zA-Z ]+(?=[^#]*##)'
    return re.sub(pattern, lambda match: match.group().replace(' ', '_'), line)


# Function to create a client object from a log entry
def create_client(entry: str, client_id: str, country: str, city: str) -> Client_Model:
    cli = Client_Model()
    cli.client_id = client_id
    cli.country = country
    cli.city = city
    cli.user_agent = str(entry.headers_in["User-Agent"])
    return cli


# Function to create a session object from a log entry
def create_session(id: Decimal) -> Session_Model:
    sess = Session_Model()
    sess.session_id = id
    return sess


# Function to create a request object from a log entry
def create_request(entry: str, id: Decimal) -> Request_Model:
    req = Request_Model()
    req.request_id = id
    req.request_time = entry.request_time
    req.request_url = str(entry.request_line)
    req.response_code = str(entry.final_status)
    req.referer = str(entry.headers_in["Referer"])
    return req


# Function to parse the log file
async def compute(file, collection: dict):
    # import parameters from json file
    parser_type, parser_format, session_time_limit, exclude_keywords = load_json_parameters()
    parser = LogParser(parser_format)
    # try to get the clients from the collection (if it exists)
    dict_client = collection
    # with open(file, "r") as f:
    f = file.read()
    for entry in f:
        # Replace spaces with underscores in the relevant portion of the line
        entry = replace_space_with_underscore(entry)
        # Check if the line is valuable
        if line_is_valuable(exclude_keywords, entry):
            entry = parser.parse(entry)

            client_id, country, city = get_id_contry_city(
                entry.remote_host)
            # If the client is not in the list, create it
            if client_id not in dict_client.keys():
                # Create User
                cli = create_client(
                    entry, client_id, country, city)

                # Create session with id 1
                session_id = Decimal("1")
                sess = create_session(session_id)

                # Create request with id 1.1
                request_id = Decimal("1.1")
                req = create_request(entry, request_id)

                sess.requests.append(req)
                cli.sessions.append(sess)
                dict_client[client_id] = cli
            else:
                cli = dict_client[client_id]
                last_req_time = cli.sessions[-1].requests[-1].request_time
                # If the request time is less than 1 hour from the previous request, add it to the same session
                if (entry.request_time - last_req_time).total_seconds() < session_time_limit:
                    # Create request with id depending on the number of requests in the session
                    request_id = cli.sessions[-1].requests[-1].request_id + \
                        Decimal("0.1")
                    req = create_request(entry, request_id)
                    # Add the request to the lastsession
                    cli.sessions[-1].requests.append(req)
                # Else, create a new session and add the request to it
                else:
                    # Create session with id depending on the last session id
                    session_id = cli.sessions[-1].session_id + Decimal("1")
                    sess = create_session(session_id)

                    # Create request with id depending on the number of session id
                    request_id = session_id + Decimal("0.1")
                    req = create_request(entry, request_id)

                    sess.requests.append(req)
                    cli.sessions.append(sess)

    # Add the new clients to the collection
    list_client = []
    for val in dict_client.values():
        list_client.append(val.dict())
    return list_client


# If run as a script, parse the log file and print the result
# if __name__ == "__main__":
#     # Parse the log file
#     myFile = io.StringIO("")
#     myFile.write("Write a line into the file\n")
#     cli = compute(myFile, {})
#     with open("src/json/clients.json", "w") as f:
#         json.dump(cli, f)
