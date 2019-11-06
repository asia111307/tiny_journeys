from start import db
from models import Tag, TagPost, Like, Comment, User, Post, Photo, Video
from flask import Blueprint, render_template, request, redirect, url_for, g, jsonify, make_response
from flask_login import login_required, current_user
from bs4 import BeautifulSoup
import datetime, re

post = Blueprint('post', __name__, template_folder='templates', static_folder='static')


@post.route('/view/<int:post_id>')
def view_post(post_id):
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


@post.route('/add', methods=['POST', 'GET'])
@login_required
def add_post():
    if request.method == 'POST':
        author = current_user.id
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
            link = url_for('post.view_post', post_id=post.id)
        return redirect(link)
    else:
        tags = Tag.query.all()
        return render_template('addpost.html', tags=tags)


@post.route('/delete/<int:post_id>')
@login_required
def delete_post(post_id):
    Post.query.filter_by(id=post_id).delete()
    Photo.query.filter_by(post_id=post_id).delete()
    Video.query.filter_by(post_id=post_id).delete()
    TagPost.query.filter_by(post=post_id).delete()
    Comment.query.filter_by(post_id=post_id).delete()
    Like.query.filter_by(post_id=post_id).delete()
    db.session.commit()
    return redirect('/')


@post.route('/edit/<int:post_id>', methods=['POST', 'GET'])
@login_required
def edit_post(post_id):
    if request.method == 'POST':
        post = Post.query.get_or_404(post_id)
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.last_modified_date = datetime.datetime.now()
        db.session.commit()
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
        return redirect(url_for('post.view_post', post_id=post.id))
    else:
        post = Post.query.get_or_404(post_id)
        author = User.query.get(post.author).username
        tags = Tag.query.all()
        tag = db.session.query(Tag, TagPost).filter(TagPost.tag == Tag.id).filter(TagPost.post == post.id).first()
        return render_template('editpost.html', post=post, author=author, tags=tags, tag=tag)


@post.route('/like/<int:user_id>/<int:post_id>', methods=['POST', 'GET'])
def like_post(user_id, post_id):
    db.session.add(Like(user_id, post_id))
    db.session.commit()
    post = Post.query.get_or_404(post_id)
    user = User.query.get(post.author)
    likes = db.session.query(Like, User).filter(Like.user_id == User.id).filter(Like.post_id == post.id).order_by(
        Like.date.desc()).all()
    return render_template('blocks/block_likes.html', user_post_likes=True, post=post, user=user, likes=likes)


@post.route('/unlike/<int:user_id>/<int:post_id>', methods=['POST', 'GET'])
def unlike_post(user_id, post_id):
    Like.query.filter(Like.post_id == post_id).filter(Like.user_id == user_id).delete()
    db.session.commit()
    post = Post.query.get_or_404(post_id)
    user = User.query.get(post.author)
    likes = db.session.query(Like, User).filter(Like.user_id == User.id).filter(Like.post_id == post.id).order_by(
        Like.date.desc()).all()
    return render_template('blocks/block_likes.html', user_post_likes=False, post=post, user=user, likes=likes)


