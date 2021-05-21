import os

SECRET_KEY = 'the random string bla bla'

SQLALCHEMY_TRACK_MODIFICATIONS = False

USER = 'root'
PASSWORD = 'password'
HOST = '127.0.0.1'
DATABASE = 'test_tickets'
SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}/{DATABASE}'

LOGGING_LEVEL = 'INFO'
