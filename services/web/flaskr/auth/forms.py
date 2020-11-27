from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class RegisterForm(FlaskForm):
    username = StringField("Username", [DataRequired()])
    password = PasswordField('Password', [DataRequired(message="Please, enter a password.")])
    confirm_password = PasswordField('Repeat pssword', [EqualTo("password", message='Passwords do not match.')])
    submit = SubmitField('Submit')


class LogInForm(FlaskForm):
    username = StringField("Username", [DataRequired()])
    password = PasswordField('Password', [DataRequired(message="Please, enter a password.")])
    submit = SubmitField('Log In')
