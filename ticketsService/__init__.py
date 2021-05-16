from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/tickets'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'the random string bla bla'
db = SQLAlchemy(app)

USER = 'root'
PASSWORD = 'password'
HOST = 'localhost'
DATABASE = 'tickets'

url = 'mysql://%s:%s@%s' % (USER, PASSWORD, HOST)
engine = db.create_engine(url, {})  # connect to server

create_str = "CREATE DATABASE IF NOT EXISTS %s ;" % (DATABASE)
engine.execute(create_str)
engine.execute("USE tickets;")
db.create_all()
db.session.commit()