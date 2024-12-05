from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

# Login form
class AccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

# Post form
class PostForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])