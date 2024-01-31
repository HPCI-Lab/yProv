import json
import datetime
import jwt
import os
from passlib.hash import bcrypt

ACCOUNT_FILE = "conf/accounts.json"
BLACKLIST_FILE = "conf/blacklist"
GRAPHS_FILE = "conf/graphs.json"


def encode_password(password: str) -> str:
    return bcrypt.hash(password)


def check_password(password: str, encoded_password: str) -> bool:
    return bcrypt.verify(password, encoded_password)


def update_file_info(file_path: str, data: dict):

    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)


def get_users_info(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as json_file:
            return json.load(json_file)
    except Exception as e:
        print(f'Error: {e}')


def is_blacklisted(token: str) -> bool:
    try:
        with open(BLACKLIST_FILE, 'r') as blacklist:
            content_set = set(line.strip() for line in blacklist)
            if token in content_set:
                return True
            else:
                return False
    except Exception as e:
        print(f'Error: {e}')


def add_to_blacklist(token: str):
    try:
        with open(BLACKLIST_FILE, 'a') as file:
            file.write(token + '\n')
    except Exception as e:
        print(f'Error: {e}')
        raise e


def is_token_valid(token: str) -> bool:
    try:
        header_data = jwt.get_unverified_header(token)
        data = jwt.decode(token, os.getenv('SECRET_KEY', "secret_key"), algorithms=[header_data['alg'], ])
        time_difference = datetime.datetime.utcfromtimestamp(data['exp']) - datetime.datetime.utcnow()
        if is_blacklisted(token) or time_difference < datetime.timedelta(minutes=5):
            return False
        else:
            return True
    except:
        return False


def check_account_valid(auth_data: dict) -> bool:
    accounts_data = get_users_info(ACCOUNT_FILE)
    if accounts_data and auth_data["user"] in accounts_data.keys():
        if check_password(auth_data["password"], accounts_data[auth_data["user"]]["password"]):
            return True
    return False


def check_user_presence(user: str) -> bool:
    accounts_data = get_users_info(ACCOUNT_FILE)
    if user in accounts_data.keys():
        return True
    return False


def add_user(auth_data: dict):
    accounts_data = get_users_info(ACCOUNT_FILE)
    if not accounts_data or not auth_data["user"] in accounts_data.keys():
        accounts_data[auth_data["user"]] = {'password': encode_password(auth_data["password"])}
        update_file_info(ACCOUNT_FILE, accounts_data)


def get_password(user: str) -> str:
    accounts_data = get_users_info(ACCOUNT_FILE)
    if user in accounts_data.keys():
        return accounts_data[user]["password"]
    else:
        return ""


def get_user(token: str) -> str:
    header_data = jwt.get_unverified_header(token)
    data = jwt.decode(token, os.getenv('SECRET_KEY', "secret_key"), algorithms=[header_data['alg'], ])
    return data['user']


def is_graph_valid(doc_id: str) -> bool:
    graphs_data = get_users_info(GRAPHS_FILE)
    if doc_id in graphs_data.keys():
        return True
    return False


def add_new_graph(user: str, doc_id: str):
    graphs_data = get_users_info(GRAPHS_FILE)
    graphs_data[doc_id] = {user: 'o'}

    update_file_info(GRAPHS_FILE, graphs_data)


def has_user_permission(user: str, doc_id: str, permissions_requested, docs=False) -> bool:
    """
    Documents
        c   r   u   d   n
    o   √   √   √   √   √
    r   √   √   x   x   x
    w   √   √   √   x   x

    Sub-elements of graph
        c   r   u   d
    o   √   √   √   √
    r   x   √   x   x
    w   √   √   √   √
    """
    graphs_data = get_users_info(GRAPHS_FILE)
    if doc_id in graphs_data.keys():
        if user in graphs_data[doc_id].keys():
            if permissions_requested == 'r':
                return True
            elif docs:
                if graphs_data[doc_id][user] == 'o':
                    return True
                elif (graphs_data[doc_id][user] == 'w' and
                      permissions_requested != 'd' and
                      permissions_requested != 'n'):
                    return True
            else:
                if (graphs_data[doc_id][user] == 'o' or
                        graphs_data[doc_id][user] == 'w'):
                    return True
    return False


def add_new_user_permission(new_user: str, doc_id: str, level: str):
    graphs_data = get_users_info(GRAPHS_FILE)
    graphs_data[doc_id][new_user] = level
    update_file_info(GRAPHS_FILE, graphs_data)
