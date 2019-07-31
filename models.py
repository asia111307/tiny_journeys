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
    profile_image = Column(String, default='')
    creation_date = Column(DateTime, default=datetime.datetime.now)
    isAdmin = Column(Boolean, default=False)
    isLocked = Column(Boolean, default=False)
    isOnline = Column(Boolean, default=False)

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'profile_image': self.profile_image,
            'creation_date': self.creation_date,
            'isAdmin': self.isAdmin,
            'isLocked': self.isLocked,
            'isOnline': self.isOnline
        }

    def __init__(self, username, password, isAdmin, profile_image):
        self.username = username
        self.password = password
        self.isAdmin = isAdmin
        self.profile_image = profile_image


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

    def __init__(self, name, source, post_id):
        self.name = name
        self.source = source
        self.post_id = post_id


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

    def __init__(self, name, source, post_id):
        self.name = name
        self.source = source
        self.post_id = post_id


class Like(db.Model):
    __tablename__ = 'like'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('user.id'))
    date = Column(DateTime, default=datetime.datetime.now)

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.author_id,
            'post_id': self.post_id,
            'date': self.date,
        }

    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id


class Tag(db.Model):
    __tablename__ = 'tag'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, default='')
    date = Column(DateTime, default=datetime.datetime.now)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date,
        }

    def __init__(self, name):
        self.name = name


class TagPost(db.Model):
    __tablename__ = 'tagpost'
    id = Column(Integer, autoincrement=True, primary_key=True)
    tag = Column(Integer, ForeignKey('tag.id'))
    post = Column(Integer, ForeignKey('post.id'))

    def to_json(self):
        return {
            'id': self.id,
            'tag': self.tag,
            'post': self.post,
        }

    def __init__(self, tag, post):
        self.tag = tag
        self.post = post
