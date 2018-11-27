from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from models import *
from flask import Markup


class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    signin = SubmitField('Signin')
    def  nouser(self, username):
        nousr = User.query.filter_by(username=username.data).first()
        if nousr is None:
            err = Markup('<span style="color:green;">This username is not in our database if you don\'t have an account you can create it now by clicking<a href="/register>here</a>"<span>')
            raise ValidationError(err)




class RegistrationForm(FlaskForm):
    fullname = StringField('fullname')
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password'), ])
    submit = SubmitField('Register')
    def validate_username(self, username):
        usr = User.query.filter_by(username=username.data).first()
        if usr is not None:
            raise ValidationError('Please use a different username.')
    def validate_email(self, email):
        usr = User.query.filter_by(email=email.data).first()
        if usr is not None:
            raise ValidationError('Please use a different email address.')


class EditForm(FlaskForm):
    fullname = StringField('fullname')
    email = StringField('Email', validators=[Email()])
    #current_password = PasswordField('Current password', validators=[DataRequired()])
    #new_password = PasswordField('New Password')
    #repeat_password = PasswordField('Repeat_password', validators=[EqualTo('new_password')])
    submit = SubmitField('Change your information')


