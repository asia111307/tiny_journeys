__author__ = 'Joanna Paliwoda'

from sqlalchemy import create_engine
import models
from start import db


def db_start():
    create_engine('sqlite:///tmp/gr_db.db', convert_unicode=True)
    db.create_all()
    db.session.commit()
    post = models.Post('Asia', 'first post', 'xyz', '24.02.2019')
    db.session.add(post)
    db.session.commit()
    comment = models.Comment('Asia', 'Polecam, fajnie tam', post.id, '24.02.2019')
    db.session.add(comment)
    db.session.commit()


db_start()
db.create_all()


