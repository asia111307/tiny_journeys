from start import db
from models import Comment, User, Post
from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import current_user

comment = Blueprint('comment', __name__, template_folder='templates', static_folder='static')


@comment.route('/add/<int:post_id>', methods=['POST', 'GET'])
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
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter(Comment.post_id == post.id).order_by(Comment.creation_date.desc()).all()
    return render_template('blocks/block_comments.html', post=post, comments=comments)
