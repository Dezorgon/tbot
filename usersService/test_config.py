import os

SECRET_KEY = 'the random string bla bla'

SQLALCHEMY_TRACK_MODIFICATIONS = False

USER = 'root'
PASSWORD = 'password'
HOST = '127.0.0.1'
DATABASE = 'test_users'
SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}/{DATABASE}'
# db_path = os.path.realpath(os.path.join(os.path.dirname(__file__), DATABASE))
# SQLALCHEMY_DATABASE_URI = 'sqlite:////1234.db'
LOGGING_LEVEL = 'INFO'
