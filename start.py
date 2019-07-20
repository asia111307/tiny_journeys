__author__ = 'Asia Paliwoda'

from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gr_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.app = app
db.init_app(app)

app.static_path = path.join(path.abspath(__file__), 'static')

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


def db_start():
    create_engine('sqlite:///tmp/gr_db.db', convert_unicode=True)
    db.create_all()
    db.session.commit()

    
from models import *
from views import *
db_start()
db.session.commit()


if __name__ == 'start':
    app.run(debug=True)

