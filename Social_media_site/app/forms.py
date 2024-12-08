from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from .models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AccountForm(FlaskForm):
    username = StringField('New Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

# Post form
class PostForm(FlaskForm):
    post = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SignupForm(FlaskForm): 
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()]) 
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')]) 
    submit = SubmitField('Sign Up') 
    
    def validate_username(self, username): 
        user = User.query.filter_by(username=username.data).first() 
        if user: 
            raise ValidationError('That username is taken. Please choose a different one.')
