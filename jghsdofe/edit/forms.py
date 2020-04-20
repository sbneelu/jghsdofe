from flask import url_for
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Email, ValidationError, EqualTo, Length

class AnnouncementForm(FlaskForm):
    content = TextAreaField('Announcement', validators=[InputRequired()])
    starred = BooleanField('Starred: ')
    submit = SubmitField('Submit')
