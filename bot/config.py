import os

SECRET_KEY = 'the random string bla bla'

USER_DB_URL = f'http://{os.environ["USERS_DB_HOST"]}:{os.environ["USERS_DB_PORT"]}/'
TICKETS_DB_URL = f'http://{os.environ["TICKETS_DB_HOST"]}:{os.environ["TICKETS_DB_PORT"]}/'
LOGGING_LEVEL = os.environ["LOGGING_LEVEL"]
