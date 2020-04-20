from flask import url_for
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FileField
from wtforms.validators import InputRequired, Email, ValidationError, EqualTo, Length, URL

class AnnouncementForm(FlaskForm):
    content = TextAreaField('Announcement', validators=[InputRequired()])
    starred = BooleanField('Starred: ')
    submit = SubmitField('Submit')


class SectionDetailsForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(max=100)])
    description = StringField('Description (optional)')
    submit = SubmitField('Submit')


class LinkDetailsForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(max=100)])
    link = StringField('Link', validators=[InputRequired(), URL(message='Invalid link. Remember to include http:// or https:// in the URL.')])
    submit = SubmitField('Submit')


class FileDetailsForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(max=100)])
    file = FileField('File', validators=[InputRequired()])
    submit = SubmitField('Submit')


class EditFileDetailsForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(max=100)])
    file = FileField('File')
    submit = SubmitField('Submit')
