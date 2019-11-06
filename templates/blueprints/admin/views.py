from start import db
from models import Tag, TagPost, Comment, User, Post
from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_login import login_required,  current_user

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


@admin.route('/panel', methods=['POST', 'GET'])
@login_required
def panel():
    if current_user.isAdmin:
        tags = Tag.query.all()
        tagposts = db.session.query(TagPost, Tag, Post).filter(TagPost.tag == Tag.id).filter(TagPost.post == Post.id).all()
        users = User.query.all()
        return render_template('admin_panel.html', tags=tags, tagposts=tagposts, users=users)
    else:
        return abort(404)


@admin.route('/add/tag', methods=['POST', 'GET'])
@login_required
def add_tag():
    if request.method == 'POST':
        tag = request.form.get('new_tag')
        db.session.add(Tag(tag))
        db.session.commit()
        return redirect(url_for('admin.panel'))
    else:
        return redirect(url_for('admin.panel'))


@admin.route('/delete/tag/<int:tag_id>', methods=['POST', 'GET'])
@login_required
def delete_tag(tag_id):
    Tag.query.filter_by(id=tag_id).delete()
    TagPost.query.filter_by(tag=tag_id).delete()
    db.session.commit()
    return redirect(url_for('admin.panel'))


@admin.route('/delete/user/<int:user_id>', methods=['POST', 'GET'])
@login_required
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect(url_for('admin.panel'))


@admin.route('/lock/user/<int:user_id>', methods=['POST', 'GET'])
@login_required
def lock_user(user_id):
    user = User.query.get(user_id)
    user.isLocked = True
    db.session.commit()
    return redirect(url_for('admin.panel'))


@admin.route('/unlock/user/<int:user_id>', methods=['POST', 'GET'])
@login_required
def unlock_user(user_id):
    user = User.query.get(user_id)
    user.isLocked = False
    db.session.commit()
    return redirect(url_for('admin.panel'))


@admin.route('/delete/comment/<int:post_id>/<int:comment_id>')
def delete_comment(post_id, comment_id):
    Comment.query.filter_by(id=comment_id).delete()
    db.session.commit()
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter(Comment.post_id == post.id).order_by(Comment.creation_date.desc()).all()
    return render_template('blocks/block_comments.html', post=post, comments=comments)
