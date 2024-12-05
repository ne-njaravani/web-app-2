from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, DateField, BooleanField
from wtforms.validators import DataRequired, Regexp, ValidationError
from datetime import datetime


# Ensure dates are valid and not in the past
def deadline_validator(form, field):
    if field.data < datetime.today().date():
        raise ValidationError('Deadline must be a future date.')


class AssessmentForm(FlaskForm):
    title = StringField(
        'Title', 
        validators=[DataRequired(message='Title is required')]
    )
    module_code = StringField(
        'Module Code', 
        validators=[DataRequired(message='Module Code is required'), 
                    Regexp(r'^[A-Z]{4}\d{4}', message='Module code must be in the format ABCD1234')
        ]
    )
    description = TextAreaField(
        'Description', 
        validators=[DataRequired(message='Description is required')]
    )
    deadline = DateField(
        'Deadline', format='%Y-%m-%d', 
        validators=[DataRequired(message='Deadline is required'), deadline_validator]
    )
    completed = BooleanField('Completed', default=False)