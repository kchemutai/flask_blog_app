from flask.helpers import flash, url_for
from flask_login.utils import login_required
from flask_wtf import form
from werkzeug.urls import url_parse
from werkzeug.utils import redirect
import app
from flask_login import current_user, login_user, logout_user
from datetime import datetime

from app import app, db
from flask import render_template, request

from app.forms import EditProfileForm, LoginForm, RegistrationForm
from app.models import User

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.commit()

@app.route('/')
@login_required
def index():
    user= {'username': 'kchemutai'}
    posts = [
        {
            'title': 'flask tutorial',
            'content': 'pyhthon flask refresher',
            'author': {'username': 'kchemutai'}
        },
        {
            'title': 'Avengers',
            'content': 'The Avengers movie was so cool!',
            'author': {'username': 'mgrinberg'}
        }
    ]
    return render_template('index.html', posts=posts)


@app.route('/login', methods=['get', 'post'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('index')
        return redirect(next_page)
 
    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['post','get'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account Successfully Created')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
        
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {
            'title': 'Beautiful Day in portland',
            'content': 'Portland, Oregon’s largest city, sits on the Columbia and Willamette rivers, in the shadow of snow-capped Mount Hood. It’s known for its parks, bridges and bicycle paths, as well as for its eco-friendliness and its microbreweries and coffeehouses',
            'author': user
        },
        {
            'title': 'Silcon valleny',
            'content': 'Silicon Valley, in the southern San Francisco Bay Area of California, is home to many start-up and global technology companies. Apple, Facebook and Google are among the most prominent. Its also the site of technology-focused institutions centered around Palo Altos Stanford University.',
            'author': user
        }
    ]
    return render_template('user.html', title='Profile', posts=posts, user=user)


@app.route('/edit_profile', methods=['get', 'post'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)