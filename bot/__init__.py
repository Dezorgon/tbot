from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'the random string bla bla'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////test.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
login_manager = LoginManager(app)
