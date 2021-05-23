import os

SECRET_KEY = 'the random string bla bla'

SQLALCHEMY_TRACK_MODIFICATIONS = False

USER = 'root'
PASSWORD = 'password'
HOST = os.environ['MYSQL_HOST']
DATABASE = os.environ['MYSQL_DATABASE']
SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}/{DATABASE}'
