from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    """
    WTForms is an instrument which makes working with forms easier
    It can:
    - Check the data;
    - Create form errors;
    - Save data storage on a server (CSRF protection)

    Each field on a form has its own class from WTForms (e.g. StringField, PasswordField ...)
    """
    username = StringField('Username: ', validators=[DataRequired(), Length(4, max=20)])
    password = PasswordField('Password: ', validators=[DataRequired(), Length(4, max=100, message='Password must be between 4 and 100 symbols!')])
    remember_me_button = BooleanField('Remember Me: ', default=False)
    submit_button = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired(), Length(4, max=20)])
    email = StringField('Email: ', validators=[DataRequired(), Email('Invalid Email!')])
    password_1 = PasswordField('Password: ', validators=[DataRequired(), Length(4, max=100, message='Password must be between 4 and 100 symbols!')])
    password_2 = PasswordField('Repeat Password: ', validators=[DataRequired(), EqualTo('password_1', message="Passwords Don't Match!")])
    submit_button = SubmitField('SignUp')





