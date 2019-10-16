from start import db, app
from models import User
from flask import Blueprint, render_template, abort, request, redirect, session
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy import exc
import os

account = Blueprint('account', __name__, template_folder='templates', static_folder='static')


@account.route('/login', methods=['POST', 'GET'])
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
                return render_template('blueprints/account/login/templates/login.html', feedback=feedback)
        except (exc.OperationalError, AttributeError):
            feedback = ''
            if request.method == 'POST':
                db.session.rollback()
                feedback = 'This username does not exist in our system.'
            return render_template('blueprints/account/login/templates/login.html', feedback=feedback)
    else:
        return render_template('blueprints/account/login/templates/login.html', feedback='')


@account.route("/logout/<int:user_id>")
@login_required
def logout(user_id):
    logout_user()
    user = User.query.get(user_id)
    user.isOnline = False
    db.session.commit()
    return redirect('/')


@account.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_again = request.form.get('password-again')
        profile_image_file = request.files['profile-image-file']
        profile_image_link = request.form.get('profile-image-link')
        all_usernames = [user.username for user in User.query.all()]
        file_src = 'https://cdn.pixabay.com/photo/2014/04/02/10/25/man-303792_960_720.png'
        if username in all_usernames:
            feedback = 'This username is already taken'
            return render_template('blueprints/account/register/templates/register.html', feedback=feedback)
        if password != password_again:
            feedback = 'Passwords do not match'
            return render_template('blueprints/account/register/templates/register.html', feedback=feedback)
        if profile_image_file:
            filename = 'profile-image-{}.jpg'.format(username)
            profile_image_file.save(os.path.join(app.root_path, 'static', 'uploads', filename))
            file_src = 'uploads/{}'.format(filename)
        if profile_image_link:
            file_src = profile_image_link
        db.session.add(User(username, password, False, file_src))
        db.session.commit()
        user = User.query.order_by(User.id.desc()).first()
        login_user(user, remember=True)
        session['logged_user'] = user.id
        user.isOnline = True
        db.session.commit()
        return redirect('/')
    else:
        return render_template('blueprints/account/register/templates/register.html')


@account.route("/profile/<username>")
@login_required
def view_profile(username):
    user = User.query.filter(User.username == username).first()
    if not user:
        return abort(404)
    return render_template('blueprints/account/profile/templates/profile.html', user=user)
