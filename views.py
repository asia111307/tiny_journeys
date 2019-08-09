#! usr/bin/ env python
# encoding: utf-8

from start import app, db
from models import User, Photo, Video, Comment, Like, Post
from flask import render_template
from flask_login import LoginManager, current_user

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "account.login"


@app.route('/')
def start():
    posts = db.session.query(User, Post).filter(Post.author == User.id).order_by(Post.creation_date.desc()).all()
    comments = user_posts = user_comments = user_videos = user_photos = likes = user_post_likes = tagposts = comments_count = ''
    users = User.query.all()
    photos = Photo.query.all()
    videos = Video.query.all()
    online_users = User.query.filter(User.isOnline == True).all()
    if posts:
        comments = [Comment.query.filter(Comment.post_id == post[1].id).order_by(Comment.creation_date.desc()).all() for post in posts]
        comments_count = sum(len(comment) for comment in comments)
        likes = [db.session.query(Like, User).filter(Like.user_id == User.id).filter(Like.post_id == post[1].id).order_by(Like.date.desc()).all() for post in posts]
    if not current_user.is_anonymous:
        user_posts = Post.query.filter(Post.author == current_user.id).all()
        user_photos = [len(Photo.query.filter(Photo.post_id == user_post.id).all()) for user_post in user_posts]
        user_videos = [len(Video.query.filter(Video.post_id == user_post.id).all()) for user_post in user_posts]
        user_comments = Comment.query.filter(Comment.author_id == current_user.id).all()
        user_post_likes = [True if Like.query.filter(Like.post_id == post[1].id).filter(Like.user_id == current_user.id).all() else False for post in posts]
    return render_template('blueprints/page_layout/home/templates/index.html', posts=posts, comments=comments, comments_count=comments_count, users=users, user_posts=user_posts, user_comments=user_comments, online_users=online_users, photos=photos, videos=videos, user_photos=user_photos, user_videos=user_videos, likes=likes, user_post_likes=user_post_likes, tagposts=tagposts)


@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
