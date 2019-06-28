#! usr/bin/ env python
# encoding: utf-8

from start import app, db
from flask import render_template, request, jsonify, redirect, url_for, Markup, session, abort, Response
from builtins import *
from sqlalchemy import exc
from models import *
import os, datetime, re
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, UserMixin

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route('/')
def start():
    posts = Post.query.order_by(Post.creation_date.desc()).all()
    prevs = nexts = comments = comments_counts = ''
    if posts:
        prevs = [Post.query.get(post.id - 1) for post in posts]
        nexts = [Post.query.get(post.id + 1) for post in posts]
        comments = [Comment.query.filter(Comment.post_id == post.id).order_by(Comment.creation_date.desc()).all() for post in posts]
        comments_counts = [len(comments[i]) for i in range(len(posts))]
    user_name = request.args.get('user_name')
    return render_template('index.html', posts=posts, prevs=prevs, nexts=nexts, comments=comments, comments_counts=comments_counts, user_name=user_name)


@app.route('/add-post')
def render_add_post():
    return render_template('addpost.html')


@app.route('/addpost', methods=['POST', 'GET'])
def add_post():
    author = request.form.get('author')
    title = request.form.get('title')
    content = request.form.get('content')
    link = '/'
    if author and title and content:
        db.session.add(Post(author, title, content))
        db.session.commit()
        post_id = Post.query.order_by(Post.id.desc()).first().id
        pat = re.compile(r'<img [^>]*src="([^"]+)')
        imgs = pat.findall(content)
        if imgs:
            for i in range(len(imgs)):
                img_title =  'Picture {} for {}'.format(i+1, title)
                db.session.add(Photo(img_title, imgs[i], post_id))
                db.session.commit()
        pat2 = re.compile(r'<iframe [^>]*src="([^"]+)')
        videos = pat2.findall(content)
        if videos:
            print(videos)
            for i in range(len(videos)):
                vid_title =  'Video {} for {}'.format(i+1, title)
                db.session.add(Video(vid_title, videos[i], post_id))
                db.session.commit()
        link = '/view/post/{}'.format(post_id)
    return redirect(link)


@app.route('/view/posts')
def render_view_posts():
    posts = Post.query.all()
    return render_template('viewposts.html', posts=posts, current_option='All')


@app.route('/view/pics')
def render_view_pics():
    pics = Photo.query.all()
    return render_template('viewpics.html', pics=pics, current_option='All')


@app.route('/view/videos')
def render_view_videos():
    videos = Video.query.all()
    return render_template('viewvideos.html', videos=videos, current_option='All')


@app.route('/view/posts/<sort_option>', methods=['POST', 'GET'])
def render_view_posts_options(sort_option):
    posts = Post.query.all()
    if sort_option == 'oldestfirst':
        posts = Post.query.order_by(Post.creation_date)
        sort_option = 'Oldest first'
    elif sort_option == 'newestfirst':
        posts = Post.query.order_by(Post.creation_date.desc())
        sort_option = 'Newest first'
    elif sort_option == 'lastweek':
        week_ago = datetime.datetime.today() - datetime.timedelta(days=7)
        posts = Post.query.filter(Post.creation_date > week_ago).order_by(Post.creation_date.desc())
        sort_option = 'Last week'
    elif sort_option == 'lastmonth':
        month_ago = datetime.datetime.today() - datetime.timedelta(days=3)
        posts = Post.query.filter(Post.creation_date > month_ago).order_by(Post.creation_date.desc())
        sort_option = 'Last month'
    return render_template('viewposts.html', posts=posts, current_option=sort_option)


@app.route('/view/post/<int:post_id>')
def render_view_post(post_id):
    post = Post.query.get_or_404(post_id)
    p_prev = Post.query.get(post_id-1)
    p_next = Post.query.get(post_id+1)
    comments = Comment.query.filter(Comment.post_id == post.id).order_by(Comment.creation_date.desc()).all()
    return render_template('view_post.html', post=post, prev=p_prev, next=p_next, comments=comments, comments_count=len(comments))


@app.route('/delete/post/<int:post_id>')
def delete_post(post_id):
    Post.query.filter_by(id=post_id).delete()
    Photo.query.filter_by(post_id=post_id).delete()
    Video.query.filter_by(post_id=post_id).delete()
    db.session.commit()
    return redirect('/')


@app.route('/delete/comment/<int:post_id>/<int:comment_id>')
def delete_comment(post_id, comment_id):
    Comment.query.filter_by(id=comment_id).delete()
    db.session.commit()
    link = '/view/post/{}'.format(post_id)
    return redirect(link)


@app.route('/edit/post/<int:post_id>')
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('editpost.html', post=post)


@app.route('/editpost/<int:post_id>', methods=['POST'])
def edit_post_id(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form.get('title')
    post.content = request.form.get('content')
    post.last_modified_date = datetime.datetime.now()
    db.session.commit()
    post_id = Post.query.order_by(Post.id.desc()).first().id
    pat = re.compile(r'<img [^>]*src="([^"]+)')
    imgs = pat.findall(post.content)
    if imgs:
        for i in range(len(imgs)):
            img_title = 'Picture {} for {}'.format(i+1, post.title)
            db.session.add(Photo(img_title, imgs[i], post_id))
            db.session.commit()
    pat2 = re.compile(r'<iframe [^>]*src="([^"]+)')
    videos = pat2.findall(post.content)
    if videos:
        for i in range(len(videos)):
            vid_title = 'Video {} for {}'.format(i+1, post.title)
            db.session.add(Video(vid_title, videos[i], post_id))
            db.session.commit()
    link = '/view/post/{}'.format(post.id)
    return redirect(link)


@app.route('/addcomment/<int:post_id>', methods=['POST', 'GET'])
def add_comment(post_id):
    author = request.form.get('author')
    content = request.form.get('content')
    db.session.add(Comment(author, content, post_id))
    db.session.commit()
    link = '/view/post/{}'.format(post_id)
    return redirect(link)


@app.route('/view/pics/<sort_option>', methods=['POST', 'GET'])
def render_view_pics_options(sort_option):
    pics = Photo.query.all()
    if sort_option == 'oldestfirst':
        pics = Photo.query.order_by(Photo.creation_date)
        sort_option = 'Oldest first'
    elif sort_option == 'newestfirst':
        pics = Photo.query.order_by(Photo.creation_date.desc())
        sort_option = 'Newest first'
    elif sort_option == 'lastweek':
        week_ago = datetime.datetime.today() - datetime.timedelta(days=7)
        pics = Photo.query.filter(Photo.creation_date > week_ago).order_by(Photo.creation_date.desc())
        sort_option = 'Last week'
    elif sort_option == 'lastmonth':
        month_ago = datetime.datetime.today() - datetime.timedelta(days=3)
        pics = Photo.query.filter(Photo.creation_date > month_ago).order_by(Photo.creation_date.desc())
        sort_option = 'Last month'
    return render_template('viewpics.html', pics=pics, current_option=sort_option)


@app.route('/view/videos/<sort_option>', methods=['POST', 'GET'])
def render_view_videos_options(sort_option):
    videos = Video.query.all()
    if sort_option == 'oldestfirst':
        videos = Video.query.order_by(Video.creation_date)
        sort_option = 'Oldest first'
    elif sort_option == 'newestfirst':
        videos = Video.query.order_by(Video.creation_date.desc())
        sort_option = 'Newest first'
    elif sort_option == 'lastweek':
        week_ago = datetime.datetime.today() - datetime.timedelta(days=7)
        videos = Video.query.filter(Video.creation_date > week_ago).order_by(Video.creation_date.desc())
        sort_option = 'Last week'
    elif sort_option == 'lastmonth':
        month_ago = datetime.datetime.today() - datetime.timedelta(days=3)
        videos = Video.query.filter(Video.creation_date > month_ago).order_by(Video.creation_date.desc())
        sort_option = 'Last month'
    return render_template('viewvideos.html', videos=videos, current_option=sort_option)


@app.route('/account')
def diaplay_login_form():
    return render_template('login.html')


@app.route('/account/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            user = User.query.filter(User.username == username).first()
            if user.password == password:
                login_user(user, remember=True)
                return redirect(request.args.get("next", "/"))
            else:
                return abort(401)
        except (exc.OperationalError, AttributeError):
            db.session.rollback()
            feedback = 'This username does not exist in our system'
            return render_template('login.html', feedback=feedback)
    else:
        return Response('''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
        ''')


@app.route("/account/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/account/create')
def diaplay_registration_form():
    return render_template('register.html')


@app.route('/account/register', methods=['POST', 'GET'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    password_again = request.form.get('password-again')
    name = request.form.get('name')
    all_usernames = [user.username for user in User.query.all()]
    if username in all_usernames:
        feedback = 'This username is already taken'
        return render_template('register.html', feedback=feedback)
    if password != password_again:
        feedback = 'Passwords do not match'
        return render_template('register.html', feedback=feedback)
    db.session.add(User(username=username, password=password, name=name))
    db.session.commit()
    return redirect('/')


@app.errorhandler(401)
def feedback(e):
    feedback = 'This password is incorrect'
    return render_template('login.html', feedback=feedback)


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
