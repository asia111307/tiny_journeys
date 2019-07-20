__author__ = 'Joanna Paliwoda'


from sqlalchemy import Column
from sqlalchemy.types import String
from sqlalchemy.types import Boolean
from sqlalchemy.types import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from flask_login import UserMixin


from start import db
import datetime


class Site(db.Model):
    __tablename__ = 'site'
    id = Column(Integer, autoincrement=True, primary_key=True)
    owner = Column(String, default="")
    online_users = Column(Integer, default=0)



class Post(db.Model):
    __tablename__ = 'post'
    id = Column(Integer, autoincrement=True, primary_key=True)
    author = Column(Integer, ForeignKey('user.id'))
    title = Column(String, default="")
    content = Column(String, default="")
    creation_date = Column(DateTime, default=datetime.datetime.now)
    last_modified_date = Column(DateTime, default=datetime.datetime.now)
    isAccepted = Column(Boolean, default=False)

    def to_json(self):
        return {
        'id': self.id,
        'author': self.author,
        'title' :self.title,
        'content': self.content,
        'creation_date': self.creation_date,
        'last_modified_date': self.last_modified_date,
        'isAccepted': self.isAccepted,
        }

    def __init__(self, author, title, content):
        self.author = author
        self.title = title
        self.content = content


class Comment(db.Model):
    __tablename__ = 'comment'
    id = Column(Integer, autoincrement=True, primary_key=True)
    author = Column(String, default='')
    author_id = Column(Integer, ForeignKey('user.id'))
    content = Column(String, default='')
    post_id = Column(Integer, ForeignKey('post.id'))
    creation_date = Column(DateTime, default=datetime.datetime.now)

    def to_json(self):
        return {
            'id': self.id,
            'author': self.author,
            'author_id': self.author_id,
            'content': self.content,
            'creation_date': self.creation_date,
            'post_id': self.post_id
        }

    def __init__(self, author, content, post_id, *author_id):
        self.author = author
        self.content = content
        self.post_id = post_id
        if author_id:
            self.author_id = author_id[0]


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String, default='')
    password = Column(String, default='')
    creation_date = Column(DateTime, default=datetime.datetime.now)
    isAdmin = Column(Boolean, default=False)
    isLocked = Column(Boolean, default=False)

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'creation_date': self.creation_date,
            'isAdmin': self.isAdmin,
            'isLocked': self.isLocked
        }

    def __init__(self, username, password, isAdmin=False):
        self.username = username
        self.password = password
        self.isAdmin = isAdmin


class Photo(db.Model):
    __tablename__ = 'photo'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, default='')
    source = Column(String, default='')
    post_id = Column(Integer, ForeignKey('post.id'))
    creation_date = Column(DateTime, default=datetime.datetime.now)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'source': self.source,
            'post_id': self.post_id,
            'creation_date': self.creation_date,
        }

    def __init__(self, name, source, *post_id):
        self.name = name
        self.source = source
        if post_id:
            self.post_id = post_id[0]


class Video(db.Model):
    __tablename__ = 'video'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, default='')
    source = Column(String, default='')
    post_id = Column(Integer, ForeignKey('post.id'))
    creation_date = Column(DateTime, default=datetime.datetime.now)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'source': self.source,
            'post_id': self.post_id,
            'creation_date': self.creation_date,
        }

    def __init__(self, name, source, *post_id):
        self.name = name
        self.source = source
        if post_id:
            self.post_id = post_id[0]
