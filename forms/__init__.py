from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='Please enter your email!')])
    password = PasswordField('Password', validators=[DataRequired(message='Please enter your password!')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')