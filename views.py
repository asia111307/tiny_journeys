#! usr/bin/ env python
# encoding: utf-8

from start import app, db
from flask import render_template, request, jsonify, redirect
from models import *
import datetime


@app.route('/add-post')
def render_add_post():
    return render_template('addpost.html')


@app.route('/view-posts')
def render_view_posts():
    posts = Post.query.all()
    return render_template('viewposts.html', posts=posts)


@app.route('/addpost', methods=['POST', 'GET'])
def add_post():
    author = request.form.get('author')
    title = request.form.get('title')
    # try:
    #     last_id = models.Post.query.order_by(models.Post.id.desc()).first().id
    # except AttributeError:
    #     last_id = 0
    # current_id = last_id + 1
    # title = '#{} {}'.format(current_id, title)
    content = request.form.get('content')
    db.session.add(Post(author, title, content))
    db.session.commit()
    return redirect('/')


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

@app.route('/')
def start():
    post = Post.query.order_by(Post.id.desc()).first()
    comments = Comment.query.filter(Comment.post_id == post.id).order_by(Comment.creation_date.desc()).all()
    return render_template('index.html', post=post, comments=comments, comments_count=len(comments))
