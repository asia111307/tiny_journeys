__author__ = 'Joanna Paliwoda'


from sqlalchemy import Column
from sqlalchemy.types import String
from sqlalchemy.types import Boolean
from sqlalchemy.types import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime


from start import db
import datetime


class Post(db.Model):
    __tablename__ = 'post'
    id = Column(Integer, autoincrement=True, primary_key=True)
    author = Column(String, default="admin")
    title = Column(String, default="")
    content = Column(String, default="")
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)
    isAccepted = Column(Boolean, default=False)

    def to_json(self):
        return {
        'id': self.id,
        'author': self.author,
        'title' :self.title,
        'content': self.content,
        'creation_date': self.creation_date,
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
    content = Column(String, default='')
    post_id = Column(Integer, ForeignKey('post.id'))
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)

    def to_json(self):
        return {
            'id': self.id,
            'author': self.author,
            'content': self.content,
            'creation_date': self.creation_date,
            'post_id': self.post_id
        }

    def __init__(self, author, content, post_id):
        self.author = author
        self.content = content
        self.post_id = post_id


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, default='')
    username = Column(String, default='')
    password = Column(String, default='')
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)
    isAdmin = Column(Boolean, default=False)
    isLocked = Column(Boolean, default=False)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'password': self.password,
            'creation_date': self.creation_date,
            'isAdmin': self.isAdmin,
            'isLocked': self.isLocked
        }

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password