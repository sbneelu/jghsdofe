from flask import abort, render_template, url_for, redirect, flash, request, Blueprint
from flask_login import current_user, login_required
from jghsdofe.models import Announcement
from jghsdofe import db
from jghsdofe.edit.forms import AnnouncementForm
import datetime

edit = Blueprint('edit', __name__)

@edit.route('/<string:level>/edit/announcements/star/<int:id>')
def star_announcement(level, id):
    if current_user.is_authenticated and getattr(current_user, level + '_access'):
        id = int(id)
        announcement = Announcement.query.get(id)
        announcement.starred = True
        db.session.commit()
    return redirect(url_for('view.announcements', level=level))


@edit.route('/<string:level>/edit/announcements/unstar/<int:id>')
def unstar_announcement(level, id):
    if current_user.is_authenticated and getattr(current_user, level + '_access'):
        id = int(id)
        announcement = Announcement.query.get(id)
        announcement.starred = False
        db.session.commit()
    return redirect(url_for('view.announcements', level=level))


@edit.route('/<string:level>/edit/announcements/delete/<int:id>')
@login_required
def delete_announcement(level, id):
    if current_user.is_authenticated and getattr(current_user, level + '_access'):
        announcement = Announcement.query.get(id)
        return render_template('edit/delete-announcement.html.j2', level=level, title='Delete announcement | ' + level.capitalize(), announcement=announcement)
    flash('You are not authorised to delete announcements for this level.', 'danger')
    return redirect(url_for('view.announcements', level=level))


@edit.route('/<string:level>/edit/announcements/delete/<int:id>/confirm')
def confirm_delete_announcement(level, id):
    if current_user.is_authenticated and getattr(current_user, level + '_access'):
        id = int(id)
        announcement = Announcement.query.get(id)
        db.session.delete(announcement)
        db.session.commit()
    return redirect(url_for('view.announcements', level=level))


@edit.route('/<string:level>/edit/announcements/new', methods=['GET', 'POST'])
@login_required
def new_announcement(level):
    if current_user.is_authenticated and getattr(current_user, level + '_access'):
        form = AnnouncementForm()
        if form.validate_on_submit():
            announcement = Announcement(content=form.content.data.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>'), starred=form.starred.data, edited=False, date_posted=datetime.datetime.utcnow(), date_edited=datetime.datetime.utcnow(), level=level)
            db.session.add(announcement)
            db.session.commit()
            return redirect(url_for('view.announcements', level=level))
        return render_template('edit/new-announcement.html.j2', level=level, title='New announcement | ' + level.capitalize(), form=form)
    flash('You are not authorised to create announcements for this level.', 'danger')
    return redirect(url_for('view.announcements', level=level))


@edit.route('/<string:level>/edit/announcements/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_announcement(level, id):
    if current_user.is_authenticated and getattr(current_user, level + '_access'):
        form = AnnouncementForm()
        announcement = Announcement.query.get(id)
        if form.validate_on_submit():
            announcement.content = form.content.data.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')
            announcement.starred = form.starred.data
            announcement.edited = True
            announcement.date_edited = datetime.datetime.utcnow()
            db.session.commit()
            return redirect(url_for('view.announcements', level=level))
        elif request.method == 'GET':
            form.content.data = announcement.content.replace('<br>', '\n').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
            form.starred.data = announcement.starred
        return render_template('edit/new-announcement.html.j2', level=level, title='New announcement | ' + level.capitalize(), form=form, announcement=announcement)
    flash('You are not authorised to edit announcements for this level.', 'danger')
    return redirect(url_for('view.announcements', level=level))
