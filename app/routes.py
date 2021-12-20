from flask.helpers import flash, url_for
from flask_login.utils import login_required
from flask_wtf import form
from werkzeug.urls import url_parse
from werkzeug.utils import redirect
import app
from flask_login import current_user, login_user, logout_user


from app import app, db
from flask import render_template, request

from app.forms import LoginForm, RegistrationForm
from app.models import User

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
        