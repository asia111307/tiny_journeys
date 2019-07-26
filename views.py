#! usr/bin/ env python
# encoding: utf-8

from start import app, db
from flask import render_template, request, jsonify, redirect, url_for, Markup, session, abort, Response
from builtins import *
from sqlalchemy import exc, text
from models import *
import os, datetime, re
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, UserMixin, current_user
from bs4 import BeautifulSoup, Tag

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route('/')
def start():
    posts = db.session.query(User, Post).filter(Post.author== User.id).order_by(Post.creation_date.desc()).all()
    prevs = nexts = comments = comments_counts = user_posts = user_comments = ''
    users = User.query.all()
    online_users = User.query.filter(User.isOnline == True).all()
    all_posts = Post.query.all()
    if posts:
        prevs = [Post.query.get(post[1].id - 1) for post in posts]
        nexts = [Post.query.get(post[1].id + 1) for post in posts]
        comments = [Comment.query.filter(Comment.post_id == post[1].id).order_by(Comment.creation_date.desc()).all() for post in posts]
        comments_counts = [len(comments[i]) for i in range(len(posts))]
    if not current_user.is_anonymous:
        user_posts = Post.query.filter(Post.author == current_user.id).all()
        user_comments = Comment.query.filter(Comment.author_id == current_user.id).all()
    return render_template('index.html', posts=posts, prevs=prevs, nexts=nexts, comments=comments, comments_counts=comments_counts, users=users, user_posts=user_posts, user_comments=user_comments, online_users=online_users, all_posts=all_posts)


@app.route('/view/<content_type>')
def render_view_content(content_type):
    contents = comments = ''
    if content_type == 'posts':
        contents = db.session.query(User, Post).filter(Post.author==User.id).order_by(Post.creation_date.desc()).all()
        comments = [len(Comment.query.filter(Comment.post_id == post[1].id).all()) for post in contents]
    elif content_type == 'photos':
        contents = Photo.query.order_by(Photo.creation_date.desc()).all()
    elif content_type == 'videos':
        contents = Video.query.order_by(Video.creation_date.desc()).all()
    return render_template('view{}.html'.format(content_type), contents=contents, current_option='Latest first', comments=comments)


@app.route('/view/<content_type>/<sort_option>', methods=['POST', 'GET'])
def render_view_photos_options(content_type, sort_option):
    content = contents = comments = ''
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
    elif sort_option == 'newestfirst':
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
    return render_template('view{}.html'.format(content_type), contents=content.all(), current_option=sort_option, comments=comments)


@app.route('/view/post/<int:post_id>')
def render_view_post(post_id):
    post = Post.query.get_or_404(post_id)
    user = User.query.get(post.author)
    p_prev = Post.query.get(post_id-1)
    p_next = Post.query.get(post_id+1)
    comments = Comment.query.filter(Comment.post_id == post.id).order_by(Comment.creation_date.desc()).all()
    return render_template('view_post.html', post=post, user=user, prev=p_prev, next=p_next, comments=comments)


def wrap(to_wrap, wrap_in):
    contents = to_wrap.replace_with(wrap_in)
    wrap_in.append(contents)


def find_all_videos(post):
    pattern = re.compile(r'<iframe [^>]*src="([^"]+)')
    video_sources = pattern.findall(post.content)
    if video_sources:
        for i in range(len(video_sources)):
            video_title = 'Video {} for {}'.format(i + 1, post.title)
            db.session.add(Video(video_title, video_sources[i], post.id))
            db.session.commit()


def find_all_images(post):
    pattern = re.compile(r'<img [^>]*src="([^"]+)')
    img_sources = pattern.findall(post.content)
    content_html = BeautifulSoup(post.content, 'html.parser')
    all_imgs = content_html.findAll('img')
    all_a_tags = content_html.findAll('a')
    if img_sources:
        for i in range(len(img_sources)):
            img_title = 'Picture {} for {}'.format(i + 1, post.title)
            db.session.add(Photo(img_title, img_sources[i], post.id))
            db.session.commit()
            if not all_imgs[i].parent.name == 'a':
                a_tag = content_html.new_tag("a")
                a_tag.attrs['href'] = img_sources[i]
                a_tag.attrs['name'] = 'image-a'
                a_tag.attrs['data-lightbox'] = post.title.replace(" ", "")
                all_imgs[i].wrap(a_tag)
    for a in all_a_tags:
        if a.get('name') == 'image-a' and not a.find('img'):
            a.decompose()
    post.content = str(content_html)
    db.session.commit()


@app.route('/add/post', methods=['POST', 'GET'])
@login_required
def add_post():
    if request.method == 'POST':
        author = session['logged_user']
        title = request.form.get('title')
        content = request.form.get('content')
        link = '/'
        if author and title and content:
            db.session.add(Post(author, title, content))
            db.session.commit()
            post = Post.query.order_by(Post.id.desc()).first()
            find_all_images(post)
            find_all_videos(post)
            link = '/view/post/{}'.format(post.id)
        return redirect(link)
    else:
        return render_template('addpost.html')


@app.route('/delete/post/<int:post_id>')
@login_required
def delete_post(post_id):
    Post.query.filter_by(id=post_id).delete()
    Photo.query.filter_by(post_id=post_id).delete()
    Video.query.filter_by(post_id=post_id).delete()
    db.session.commit()
    return redirect('/')


@app.route('/edit/post/<int:post_id>', methods=['POST', 'GET'])
@login_required
def edit_post_id(post_id):
    if request.method == 'POST':
        post = Post.query.get_or_404(post_id)
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.last_modified_date = datetime.datetime.now()
        db.session.commit()
        post = Post.query.order_by(Post.id.desc()).first()
        Photo.query.filter_by(post_id=post.id).delete()
        find_all_images(post)
        Video.query.filter_by(post_id=post.id).delete()
        find_all_videos(post)
        link = '/view/post/{}'.format(post.id)
        return redirect(link)
    else:
        post = Post.query.get_or_404(post_id)
        author = User.query.get(post.author).username
        return render_template('editpost.html', post=post, author=author)


@app.route('/add/comment/<int:post_id>', methods=['POST', 'GET'])
def add_comment(post_id):
    author = request.form.get('author')
    content = request.form.get('content')
    if not current_user.is_authenticated:
        author = '{} (anonymous)'.format(author)
        db.session.add(Comment(author, content, post_id))
    else:
        author_id = User.query.filter(User.username == author).first().id
        db.session.add(Comment(author, content, post_id, author_id))
    db.session.commit()
    link = '/view/post/{}'.format(post_id)
    return redirect(link)


@app.route('/delete/comment/<int:post_id>/<int:comment_id>')
def delete_comment(post_id, comment_id):
    Comment.query.filter_by(id=comment_id).delete()
    db.session.commit()
    link = '/view/post/{}'.format(post_id)
    return redirect(link)


@app.route('/account/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            user = User.query.filter(User.username == username).first()
            if user.password == password:
                login_user(user, remember=True)
                session['logged_user'] = user.id
                user.isOnline = True
                db.session.commit()
                return redirect(request.args.get("next", '/'))
            else:
                feedback = 'This password is incorrect.'
                return render_template('login.html', feedback=feedback)
        except (exc.OperationalError, AttributeError):
            feedback = ''
            if request.method == 'POST':
                db.session.rollback()
                feedback = 'This username does not exist in our system.'
            return render_template('login.html', feedback=feedback)
    else:
        return render_template('login.html', feedback='')


@app.route("/account/logout/<int:user_id>")
@login_required
def logout(user_id):
    logout_user()
    user = User.query.get(user_id)
    user.isOnline = False
    db.session.commit()
    return redirect('/')


@app.route('/account/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_again = request.form.get('password-again')
        all_usernames = [user.username for user in User.query.all()]
        if username in all_usernames:
            feedback = 'This username is already taken'
            return render_template('register.html', feedback=feedback)
        if password != password_again:
            feedback = 'Passwords do not match'
            return render_template('register.html', feedback=feedback)
        db.session.add(User(username=username, password=password))
        db.session.commit()
        user = User.query.order_by(User.id.desc()).first()
        login_user(user, remember=True)
        session['logged_user'] = user.id
        user.isOnline = True
        db.session.commit()
        return redirect('/')
    else:
        return render_template('register.html')


@app.route("/profile/<username>")
@login_required
def view_profile(username):
    user = User.query.filter(User.username==username).first()
    if not user:
        return abort(404)
    return render_template('profile.html', user=user)


@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
