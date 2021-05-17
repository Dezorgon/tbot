import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


USER = 'root'
PASSWORD = 'password'
HOST = os.environ['MYSQL_HOST']
DATABASE = os.environ['MYSQL_DATABASE']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}/{DATABASE}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'the random string bla bla'
db = SQLAlchemy(app)

url = 'mysql+mysqlconnector://%s:%s@%s' % (USER, PASSWORD, HOST)
engine = db.create_engine(url, {})

create_str = "CREATE DATABASE IF NOT EXISTS %s ;" % (DATABASE)
engine.execute(create_str)
engine.execute(f"USE {DATABASE};")
db.create_all()
db.session.commit()
