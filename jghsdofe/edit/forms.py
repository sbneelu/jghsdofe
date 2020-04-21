from flask import url_for
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FileField, DateField, HiddenField
from wtforms.validators import InputRequired, Email, ValidationError, EqualTo, Length, URL, Optional


class AlsoHasData(object):
    """
    Compares the values of two fields.
    :param fieldname:
        The name of the other field to compare to.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated with `%(other_label)s` and `%(other_name)s` to provide a
        more helpful error.
    """
    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)
        if other.data and not field.data:
            d = {
                'other_label': hasattr(other, 'label') and other.label.text or self.fieldname,
                'other_name': self.fieldname
            }
            message = self.message
            if message is None:
                message = 'End Time required if End Date filled'

            raise ValidationError(message)


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


class Time24h(object):
    """
    Compares the values of two fields.
    :param fieldname:
        The name of the other field to compare to.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated with `%(other_label)s` and `%(other_name)s` to provide a
        more helpful error.
    """
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if field.data:
            error = True
            if field.data.count(':') == 1:
                hour, minute = field.data.split(':')
                if is_int(hour) and is_int(minute):
                    hour = int(hour)
                    minute = int(minute)
                    if hour >= 0 and hour <= 23 and minute >= 0 and minute <= 59:
                        error = False

            message = self.message
            if message is None:
                message = 'Invalid time. Make sure the time format is HH:MM in 24-hour time, for example 16:21 for 4:21pm.'

            if error:
                raise ValidationError(message)


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


class EventForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(max=32)])
    start_date = DateField('Start Date', validators=[InputRequired()], format='%d/%m/%Y')
    start_time = StringField('Start Time', validators=[InputRequired(), Time24h()])
    end_date = DateField('End Date (optional)', validators=[Optional()], format='%d/%m/%Y')
    end_time = StringField('End Time (required if End Date filled)', validators=[AlsoHasData('end_date'), Time24h()])
    location = StringField('Location')
    description = StringField('Description')
    submit = SubmitField('Submit')


class OrderForm(FlaskForm):
    order = HiddenField('')
    submit = SubmitField('Submit')
