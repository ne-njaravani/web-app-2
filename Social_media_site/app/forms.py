from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User

# Login form
class AccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Post form
class PostForm(FlaskForm):
    post = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm): 
    comment = TextAreaField('Content', validators=[DataRequired()]) 
    submit = SubmitField('Submit')

class SignupForm(FlaskForm): 
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)]) 
    email = StringField('Email', validators=[DataRequired(), Email()]) 
    password = PasswordField('Password', validators=[DataRequired()]) 
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')]) 
    submit = SubmitField('Sign Up') 
    
    def validate_username(self, username): 
        user = User.query.filter_by(username=username.data).first() 
        if user: 
            raise ValidationError('That username is taken. Please choose a different one.') 
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first() 
        if user: raise ValidationError('That email is already in use. Please choose a different one.')
