import duckdb
import pandas as pd
import hashlib
import secrets
import datetime
from .errors import InvalidCredentialsError


def md5_hash(string: str) -> str:
    return hashlib.md5(string.encode()).hexdigest()


class User:
    def __init__(self, username, display_name, permissions, created, last_login, last_op):
        self.username = username
        self.display_name = display_name
        self.permissions = permissions.split(',')
        self.created = created
        self.last_login = last_login
        self.last_op = last_op


class Session(User):
    def __init__(self, username, display_name, permissions, created, last_login, last_op):
        super().__init__(username, display_name, permissions, created, last_login, last_op)
        self.session_start = datetime.datetime.now()
        self.session_id = secrets.token_urlsafe(32)


def login(login_str, pass_str):
    # Connect to the DuckDB database
    con = duckdb.connect()
    df = pd.read_parquet('./hive/personnel.parquet')
    con.register('personnel', df)

    hashed_pass = md5_hash(pass_str)
    # Query the user details
    query = f"""
    SELECT UserName, DisplayName, Permissions, Created, LastLogin, LastOP
    FROM personnel
    WHERE UserName = '{login_str}' AND Password = '{hashed_pass}'
    """

    result = con.execute(query).fetchdf()

    if not result.empty:
        user_data = result.iloc[0]
        user = Session(
            username=user_data['UserName'],
            display_name=user_data['DisplayName'],
            permissions=user_data['Permissions'],
            created=user_data['Created'],
            last_login=user_data['LastLogin'],
            last_op=user_data['LastOP']
        )
        return user
    else:
        raise InvalidCredentialsError()
