import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app(config):
    app = Flask(__name__)
    app.config.from_pyfile(config)
    return app


def create_db(app):
    db = SQLAlchemy(app)

    db_name = app.config['DATABASE']

    # import mysql.connector
    #
    # mydb = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     password="password"
    # )
    #
    # mycursor = mydb.cursor()
    #
    # mycursor.execute("CREATE DATABASE test_users")

    engine = db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'], {})

    create_str = "CREATE DATABASE IF NOT EXISTS %s ;" % db_name
    engine.execute(create_str)
    engine.execute(f"USE {db_name};")
    db.create_all()
    db.session.commit()

    return db


app = create_app('config.py')
db = create_db(app)
