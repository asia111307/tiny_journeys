from start import db
from models import Comment, User
from flask import Blueprint, request, redirect, url_for
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
    return redirect(url_for('post.view_post', post_id=post_id))
