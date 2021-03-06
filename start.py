__author__ = 'Asia Paliwoda'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_migrate import Migrate
from os import path

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gr_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy()
db.app = app
db.init_app(app)

app.static_path = path.join(path.abspath(__file__), 'static')

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

migrate = Migrate(app, db)


def db_start():
    create_engine('sqlite:///tmp/gr_db.db', convert_unicode=True)
    db.create_all()
    db.session.commit()

    
from views import *
db_start()
db.session.commit()

from models import User
user_admin = User.query.filter(User.username == 'admin').first()
if not user_admin:
    db.session.add(User(username='admin', password='password', isAdmin=True))
db.session.commit()

with app.app_context():
    from templates.blueprints.admin.views import admin
    from templates.blueprints.single_post.views import post
    from templates.blueprints.comments.views import comment
    from templates.blueprints.account.views import account
    from templates.blueprints.view_content.views import view
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(post, url_prefix='/post')
    app.register_blueprint(comment, url_prefix='/comment')
    app.register_blueprint(account, url_prefix='/account')
    app.register_blueprint(view, url_prefix='/view')

if __name__ == 'start':
    app.run(debug=True)

