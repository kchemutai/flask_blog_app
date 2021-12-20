from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from app.models import User

class LoginForm(FlaskForm):
    username= StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


    def validate_username(self, username):
        user_name = User.query.filter_by(username=username.data).first()
        if user_name is not None:
            raise ValidationError('Username already taken, Please choose another')

    def validate_email(self, email):
        user_mail = User.query.filter_by(email=email.data).first()
        if user_mail is not None:
            raise ValidationError('Email already used, Please choose another')
