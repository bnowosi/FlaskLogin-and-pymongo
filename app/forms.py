from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, validators
from wtforms.validators import DataRequired

class LoginForm(Form):
    """Login form to access writing and settings pages"""

    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegistrationForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.Length(min=6, max=35)])
    confirm_password = PasswordField('Confirm Password', 
    [validators.DataRequired(),validators.EqualTo('password', message='Passwords do not match')])
    confirm = PasswordField('Repeat Password')