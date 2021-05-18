import os

SECRET_KEY = 'the random string bla bla'

USER_DB_URL = f'http://{os.environ["USERS_DB_HOST"]}:81/'
TICKETS_DB_URL = f'http://{os.environ["TICKETS_DB_HOST"]}:80/'
