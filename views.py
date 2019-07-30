#! usr/bin/ env python
# encoding: utf-8

from start import app, db
from flask import render_template, request, jsonify, redirect, url_for, Markup, session, abort, Response, json
from builtins import *
from sqlalchemy import exc, text
from models import *
import os, datetime, re
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, UserMixin, current_user
from bs4 import BeautifulSoup


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route('/')
def start():
    posts = db.session.query(User, Post).filter(Post.author == User.id).order_by(Post.creation_date.desc()).all()
    comments = user_posts = user_comments = user_videos = user_photos = likes = user_post_likes = tagposts = ''
    users = User.query.all()
    photos = Photo.query.all()
    videos = Video.query.all()
    online_users = User.query.filter(User.isOnline == True).all()
    if posts:
        comments = [Comment.query.filter(Comment.post_id == post[1].id).order_by(Comment.creation_date.desc()).all() for post in posts]
        likes = [db.session.query(Like, User).filter(Like.user_id == User.id).filter(Like.post_id == post[1].id).order_by(Like.date.desc()).all() for post in posts]
    if not current_user.is_anonymous:
        user_posts = Post.query.filter(Post.author == current_user.id).all()
        user_photos = [len(Photo.query.filter(Photo.post_id == user_post.id).all()) for user_post in user_posts]
        user_videos = [len(Video.query.filter(Video.post_id == user_post.id).all()) for user_post in user_posts]
        user_comments = Comment.query.filter(Comment.author_id == current_user.id).all()
        user_post_likes = [True if Like.query.filter(Like.post_id == post[1].id).filter(Like.user_id == current_user.id).all() else False for post in posts]
    return render_template('index.html', posts=posts, comments=comments, users=users, user_posts=user_posts, user_comments=user_comments, online_users=online_users, photos=photos, videos=videos, user_photos=user_photos, user_videos=user_videos, likes=likes, user_post_likes=user_post_likes, tagposts=tagposts)


@app.route('/view/<content_type>')
def render_view_content(content_type):
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


@app.route('/view/<content_type>/<sort_option>', methods=['POST', 'GET'])
def render_view_photos_options(content_type, sort_option):
    content = contents = comments = ''
    if content_type not in ('photos', 'videos', 'posts') or sort_option not in ('oldestfirst', 'newestfirst', 'lastweek', 'lastmonth'):
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
        likes = [len(Like.query.filter(Like.post_id == post[1].id).all()) for post in content.all()]
        # if sort_option == 'mostcommented':
        #     content = db.session.query(User, Post, Comment, func.sum(Post.id).label('total')).filter(Post.author == User.id).filter(Comment.post_id == Post.id).group_by('')
        #     sort_option = 'Most commentedt'
        # if sort_option == 'mostlikes':
        #     content = db.session.query(User, Post).filter(Post.author == User.id).order_by(Post.creation_date)
        #     sort_option = 'Most liked'

    return render_template('view{}.html'.format(content_type), contents=content.all(), current_option=sort_option, comments=comments)


@app.route('/view/post/<int:post_id>')
def render_view_post(post_id):
    post = Post.query.get_or_404(post_id)
    user = User.query.get(post.author)
    p_prev = Post.query.get(post_id-1)
    p_next = Post.query.get(post_id+1)
    comments = Comment.query.filter(Comment.post_id == post.id).order_by(Comment.creation_date.desc()).all()
    likes = db.session.query(Like, User).filter(Like.user_id == User.id).filter(Like.post_id == post.id).order_by(Like.date.desc()).all()
    tag = db.session.query(Tag, TagPost).filter(TagPost.tag == Tag.id).filter(TagPost.post == post.id).first()
    user_post_likes = ''
    if current_user.is_authenticated:
        user_post_likes = True if Like.query.filter(Like.post_id == post.id).filter(Like.user_id == current_user.id).all() else False
    return render_template('view_post.html', post=post, user=user, prev=p_prev, next=p_next, comments=comments, likes=likes, user_post_likes=user_post_likes, tag=tag)


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
        tag = request.form.get('tag')
        link = '/'
        if author and title and content:
            db.session.add(Post(author, title, content))
            db.session.commit()
            post = Post.query.order_by(Post.id.desc()).first()
            if tag:
                tag_db = Tag.query.filter(Tag.name == tag).first()
                db.session.add(TagPost(tag_db.id, post.id))
                db.session.commit()
            find_all_images(post)
            find_all_videos(post)
            link = '/view/post/{}'.format(post.id)
        return redirect(link)
    else:
        tags = Tag.query.all()
        return render_template('addpost.html', tags=tags)


@app.route('/admin/panel', methods=['POST', 'GET'])
@login_required
def admin_panel():
    if current_user.isAdmin:
        tags = Tag.query.all()
        tagposts = db.session.query(TagPost, Tag, Post).filter(TagPost.tag == Tag.id).filter(TagPost.post == Post.id).all()
        return render_template('admin_panel.html', tags=tags, tagposts=tagposts)
    else:
        return abort(404)


@app.route('/add/tag', methods=['POST', 'GET'])
@login_required
def add_tag():
    if request.method == 'POST':
        tag = request.form.get('new_tag')
        print(tag)
        db.session.add(Tag(tag))
        db.session.commit()
        return redirect('/admin/panel')
    else:
        return redirect('/admin/panel')


@app.route('/delete/post/<int:post_id>')
@login_required
def delete_post(post_id):
    Post.query.filter_by(id=post_id).delete()
    Photo.query.filter_by(post_id=post_id).delete()
    Video.query.filter_by(post_id=post_id).delete()
    TagPost.query.filter_by(post=post_id).delete()
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
        tag = request.form.get('tag')
        if tag:
            tag_db = Tag.query.filter(Tag.name == tag).first()
            TagPost.query.filter(TagPost.post == post.id).delete()
            db.session.add(TagPost(tag_db.id, post.id))
            db.session.commit()
        Photo.query.filter_by(post_id=post.id).delete()
        find_all_images(post)
        Video.query.filter_by(post_id=post.id).delete()
        find_all_videos(post)
        link = '/view/post/{}'.format(post.id)
        return redirect(link)
    else:
        post = Post.query.get_or_404(post_id)
        author = User.query.get(post.author).username
        tags = Tag.query.all()
        tag = db.session.query(Tag, TagPost).filter(TagPost.tag == Tag.id).filter(TagPost.post == post.id).first()[0]
        return render_template('editpost.html', post=post, author=author, tags=tags, tag=tag)


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


@app.route('/like/post/<int:user_id>/<int:post_id>')
def like(user_id, post_id):
    db.session.add(Like(user_id, post_id))
    db.session.commit()
    link = '/view/post/{}'.format(post_id)
    return redirect(link)


@app.route('/unlike/post/<int:user_id>/<int:post_id>')
def unlike(user_id, post_id):
    Like.query.filter(Like.post_id == post_id).filter(Like.user_id == user_id).delete()
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
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
