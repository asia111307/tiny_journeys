from start import db
from models import Comment, User, Post, Photo, Video
from flask import Blueprint, render_template, abort
import datetime

view = Blueprint('view', __name__, template_folder='templates', static_folder='static')


@view.route('/<content_type>')
def view_content(content_type):
    contents = comments = likes = ''
    if content_type == 'posts':
        contents = db.session.query(User, Post).filter(Post.author==User.id).order_by(Post.creation_date.desc()).all()
        comments = [len(Comment.query.filter(Comment.post_id == post[1].id).all()) for post in contents]
        # likes = [len(Like.query.filter(Like.post_id == post[1].id).all()) for post in contents]
    elif content_type == 'photos':
        contents = Photo.query.order_by(Photo.creation_date.desc()).all()
    elif content_type == 'videos':
        contents = Video.query.order_by(Video.creation_date.desc()).all()
    else:
        return abort(404)
    return render_template('view{}.html'.format(content_type), contents=contents, current_option='Latest first', comments=comments)


@view.route('/<content_type>/<sort_option>', methods=['POST', 'GET'])
def view_content_options(content_type, sort_option):
    content = contents = comments = ''
    if content_type not in ('photos', 'videos', 'posts') or sort_option not in ('oldestfirst', 'latestfirst', 'lastweek', 'lastmonth'):
        return abort(404)
    if content_type == 'photos':
        contents = Photo
    elif content_type == 'videos':
        contents = Video
    if sort_option == 'oldestfirst':
        if content_type == 'posts':
            content = db.session.query(User, Post).filter(Post.author == User.id).order_by(Post.creation_date)
        else:
            content = contents.query.order_by(contents.creation_date)
        sort_option = 'Oldest first'
    elif sort_option == 'latestfirst':
        if content_type == 'posts':
            content = db.session.query(User, Post).filter(Post.author == User.id).order_by(Post.creation_date.desc())
        else:
            content = contents.query.order_by(contents.creation_date.desc())
        sort_option = 'Latest first'
    elif sort_option == 'lastweek':
        week_ago = datetime.datetime.today() - datetime.timedelta(days=7)
        if content_type == 'posts':
            content = db.session.query(User, Post).filter(Post.author == User.id).filter(Post.creation_date > week_ago).order_by(Post.creation_date.desc())
        else:
            content = contents.query.filter(contents.creation_date > week_ago).order_by(contents.creation_date.desc())
        sort_option = 'Last week'
    elif sort_option == 'lastmonth':
        month_ago = datetime.datetime.today() - datetime.timedelta(days=3)
        if content_type == 'posts':
            content = db.session.query(User, Post).filter(Post.author == User.id).filter(Post.creation_date > month_ago).order_by(Post.creation_date.desc())
        else:
            content = contents.query.filter(contents.creation_date > month_ago).order_by(contents.creation_date.desc())
        sort_option = 'Last month'
    if content_type == 'posts':
        comments = [len(Comment.query.filter(Comment.post_id == post[1].id).all()) for post in content.all()]
        # likes = [len(Like.query.filter(Like.post_id == post[1].id).all()) for post in content.all()]
        # if sort_option == 'mostcommented':
        #     content = db.session.query(User, Post, Comment, func.sum(Post.id).label('total')).filter(Post.author == User.id).filter(Comment.post_id == Post.id).group_by('')
        #     sort_option = 'Most commentedt'
        # if sort_option == 'mostlikes':
        #     content = db.session.query(User, Post).filter(Post.author == User.id).order_by(Post.creation_date)
        #     sort_option = 'Most liked'
    return render_template('view{}.html'.format(content_type), contents=content.all(), current_option=sort_option, comments=comments, sorting=True)

