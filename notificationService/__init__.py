from sqlalchemy import create_engine
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# app.config.from_pyfile('config.py')
#
# CONN_STR = "mysql+mysqlconnector://{0}:{1}@{2}:{3}" \
#     .format(app.config['MYSQL_USER'], app.config['MYSQL_PASSWORD'], app.config['MYSQL_HOST'], app.config['MYSQL_PORT'])
# CONN_STR_W_DB = CONN_STR + '/' + app.config['MYSQL_DB_NAME']
# app.config['CONN_STR'] = CONN_STR
# app.config['CONN_STR_W_DB'] = CONN_STR_W_DB
#
# print(app.config['CONN_STR'])
# mysql_engine = create_engine(app.config['CONN_STR'])
# mysql_engine.execute("CREATE DATABASE IF NOT EXISTS {0}".format(app.config['MYSQL_DB_NAME']))
#
# app.config['SQLALCHEMY_DATABASE_URI'] = app.config['CONN_STR_W_DB']
# db = SQLAlchemy(app)
#


