#! usr/bin/ env python
# encoding: utf-8

from start import app, db
from flask import render_template, request, jsonify, redirect, url_for, Markup
from models import *
import os
import datetime


@app.route('/')
def start():
    post = Post.query.order_by(Post.id.desc()).first()
    p_prev = Post.query.get(post.id - 1)
    p_next = Post.query.get(post.id + 1)
    comments = Comment.query.filter(Comment.post_id == post.id).order_by(Comment.creation_date.desc()).all()
    return render_template('index.html', post=post, prev=p_prev, next=p_next, comments=comments, comments_count=len(comments))


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
        link = '/view/post/{}'.format(Post.query.order_by(Post.id.desc()).first().id)
    return redirect(link)


@app.route('/view')
def render_view_posts():
    posts = Post.query.all()
    return render_template('viewposts.html', posts=posts)


@app.route('/view/<sort_option>', methods=['POST', 'GET'])
def render_view_posts_options(sort_option):
    if sort_option == 'oldestfirst':
        posts = Post.query.order_by(Post.creation_date)
        sort_option = 'Oldest first'
    elif sort_option == 'newestfirst':
        posts = Post.query.order_by(Post.creation_date.desc())
        sort_option = 'Newest first'
    elif sort_option == 'oneperpage':
        sort_option = 'One per page'
        posts = Post.query.all()
    elif sort_option == 'lastweek':
        week_ago = datetime.datetime.today() - datetime.timedelta(days=7)
        posts = Post.query.filter(Post.creation_date > week_ago).order_by(Post.creation_date.desc())
        sort_option = 'Last week'
    elif sort_option == 'lastmonth':
        month_ago = datetime.datetime.today() - datetime.timedelta(days=3)
        posts = Post.query.filter(Post.creation_date > month_ago).order_by(Post.creation_date.desc())
        sort_option = 'Last month'
    else:
        posts = Post.query.all()
        sort_option = 'Not set'
    return render_template('viewposts.html', posts=posts, current_option=sort_option)


@app.route('/view/post/<int:post_id>')
def render_view_post(post_id):
    post = Post.query.get(post_id)
    p_prev = Post.query.get(post_id-1)
    p_next = Post.query.get(post_id+1)
    comments = Comment.query.filter(Comment.post_id == post.id).order_by(Comment.creation_date.desc()).all()
    return render_template('view_post.html', post=post, prev=p_prev, next=p_next, comments=comments, comments_count=len(comments))


@app.route('/addcomment/<int:post_id>', methods=['POST', 'GET'])
def add_comment(post_id):
    author = request.form.get('author')
    content = request.form.get('content')
    db.session.add(Comment(author, content, post_id))
    db.session.commit()
    return redirect('/')


# @app.route('/products/<int:id>', methods=['GET'])
# def add(id):
#     product = models.Product.query.get_or_404(id)
#     return jsonify(products.to_json)
#
#
# @app.route('/products', methods=['POST'])
# def edit(content):
#     data = request.json()
#     product = models.Post(**data)
#     db.session.add(product)
#     db.session.commit()
#     return jsonify([
#         'created': True,
#     'id': 0;
#     ])




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