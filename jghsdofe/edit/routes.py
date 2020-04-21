from flask import abort, render_template, url_for, redirect, flash, request, Blueprint, current_app
from flask_login import current_user, login_required
from jghsdofe.models import Announcement, Section, Link, Event
from jghsdofe import db
from jghsdofe.edit.forms import AnnouncementForm, SectionDetailsForm, LinkDetailsForm, FileDetailsForm, EditFileDetailsForm, EventForm
import datetime
import os
from werkzeug import secure_filename
from urllib.parse import unquote


edit = Blueprint('edit', __name__)


def html_escape(s):
    if s is None:
        return None
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')

def html_unescape(s):
    if s is None:
        return None
    return s.replace('<br>', '\n').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')


@edit.route('/<string:level>/edit/announcements/star/<int:id>')
def star_announcement(level, id):
    announcement = Announcement.query.get(id)
    if not announcement:
        flash('Invalid Announcement.', 'danger')
        return redirect(url_for('view.announcements', level=level))
    if current_user.is_authenticated and getattr(current_user, level + '_access') and announcement.level == level:
        announcement.starred = True
        db.session.commit()
    return redirect(url_for('view.announcements', level=level))


@edit.route('/<string:level>/edit/announcements/unstar/<int:id>')
def unstar_announcement(level, id):
    announcement = Announcement.query.get(id)
    if not announcement:
        flash('Invalid Announcement.', 'danger')
        return redirect(url_for('view.announcements', level=level))
    if current_user.is_authenticated and getattr(current_user, level + '_access') and announcement.level == level:
        announcement.starred = False
        db.session.commit()
    return redirect(url_for('view.announcements', level=level))


@edit.route('/<string:level>/edit/announcements/delete/<int:id>')
@login_required
def delete_announcement(level, id):
    announcement = Announcement.query.get(id)
    if not announcement:
        flash('Invalid Announcement.', 'danger')
        return redirect(url_for('view.announcements', level=level))
    if current_user.is_authenticated and getattr(current_user, level + '_access') and announcement.level == level:
        return render_template('edit/delete-announcement.html.j2', level=level, title='Delete announcement | ' + level.capitalize(), announcement=announcement)
    flash('You are not authorised to delete announcements for this level.', 'danger')
    return redirect(url_for('view.announcements', level=level))


@edit.route('/<string:level>/edit/announcements/delete/<int:id>/confirm')
def confirm_delete_announcement(level, id):
    announcement = Announcement.query.get(id)
    if not announcement:
        flash('Invalid Announcement.', 'danger')
        return redirect(url_for('view.announcements', level=level))
    if current_user.is_authenticated and getattr(current_user, level + '_access') and announcement.level == level:
        db.session.delete(announcement)
        db.session.commit()
    return redirect(url_for('view.announcements', level=level))


@edit.route('/<string:level>/edit/announcements/new', methods=['GET', 'POST'])
@login_required
def new_announcement(level):
    if current_user.is_authenticated and getattr(current_user, level + '_access'):
        form = AnnouncementForm()
        if form.validate_on_submit():
            announcement = Announcement(content=html_escape(form.content.data), starred=form.starred.data, edited=False, date_posted=datetime.datetime.utcnow(), date_edited=datetime.datetime.utcnow(), level=level)
            db.session.add(announcement)
            db.session.commit()
            return redirect(url_for('view.announcements', level=level))
        return render_template('edit/new-announcement.html.j2', level=level, title='New announcement | ' + level.capitalize(), form=form)
    flash('You are not authorised to create announcements for this level.', 'danger')
    return redirect(url_for('view.announcements', level=level))


@edit.route('/<string:level>/edit/announcements/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_announcement(level, id):
    announcement = Announcement.query.get(id)
    if not announcement:
        flash('Invalid Announcement.', 'danger')
        return redirect(url_for('view.announcements', level=level))
    if current_user.is_authenticated and getattr(current_user, level + '_access') and announcement.level == level:
        form = AnnouncementForm()

        if form.validate_on_submit():
            announcement.content = html_escape(form.content.data)
            announcement.starred = form.starred.data
            announcement.edited = True
            announcement.date_edited = datetime.datetime.utcnow()
            db.session.commit()
            return redirect(url_for('view.announcements', level=level))
        elif request.method == 'GET':
            form.content.data = html_unescape(announcement.content)
            form.starred.data = announcement.starred
        return render_template('edit/new-announcement.html.j2', level=level, title='New announcement | ' + level.capitalize(), form=form, announcement=announcement)
    flash('You are not authorised to edit announcements for this level.', 'danger')
    return redirect(url_for('view.announcements', level=level))


@edit.route('/<string:level>/edit/links/new/section', methods=['GET', 'POST'])
@login_required
def new_section(level):
    if current_user.is_authenticated and getattr(current_user, level + '_access'):
        form = SectionDetailsForm()
        if form.validate_on_submit():
            last_section = Section.query.filter_by(level=level).order_by(Section.order.desc()).first()
            order = last_section.order + 1 if last_section else 1
            section = Section(level=level, title=html_escape(form.title.data), description=html_escape(form.description.data), order=order)
            db.session.add(section)
            db.session.commit()
            return redirect(url_for('edit.edit_section', level=level, id=section.id))
        return render_template('edit/new-section.html.j2', level=level, title='New section | ' + level.capitalize(), form=form)
    flash('You are not authorised to create sections for this level.', 'danger')
    return redirect(url_for('view.links', level=level))


@edit.route('/<string:level>/edit/links/edit/section/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_section(level, id):
    section = Section.query.get(id)
    if not section:
        flash('Invalid section.', 'danger')
        return redirect(url_for('view.links', level=level))
    if current_user.is_authenticated and getattr(current_user, level + '_access') and section.level == level:
        links = Link.query.filter_by(section_id=section.id).all()
        links.sort(key=lambda l: l.order)
        return render_template('edit/edit-section.html.j2', level=level, title='Edit section | ' + level.capitalize(), section=section, links=links)
    flash('You are not authorised to edit sections for this level.', 'danger')
    return redirect(url_for('view.links', level=level))


@edit.route('/<string:level>/edit/links/delete/section/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_section(level, id):
    section = Section.query.get(id)
    if not section:
        flash('Invalid section.', 'danger')
        return redirect(url_for('view.links', level=level))
    if current_user.is_authenticated and getattr(current_user, level + '_access') and section.level == level:

        links = Link.query.filter_by(section_id=section.id).all()
        links.sort(key=lambda l: l.order)
        return render_template('edit/delete-section.html.j2', level=level, title='Delete section | ' + level.capitalize(), section=section, links=links)
    flash('You are not authorised to delete sections for this level.', 'danger')
    return redirect(url_for('view.links', level=level))


@edit.route('/<string:level>/edit/links/delete/section/<int:id>/confirm', methods=['GET', 'POST'])
@login_required
def confirm_delete_section(level, id):
    section = Section.query.get(id)
    if not section:
        flash('Invalid section.', 'danger')
        return redirect(url_for('view.links', level=level))
    if current_user.is_authenticated and getattr(current_user, level + '_access') and section.level == level:
        section = Section.query.get(id)
        db.session.delete(section)
        links = Link.query.filter_by(section_id=id)
        for link in links:
            if link.is_doc:
                url = unquote(link.url).split('/')
                filename = ''.join(url[3:])
                os.remove(os.path.join(current_app.root_path, 'files', level, filename))
            db.session.delete(link)
        db.session.commit()
    return redirect(url_for('view.links', level=level))


@edit.route('/<string:level>/edit/links/edit/section/details/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_section_details(level, id):
    section = Section.query.get(id)
    if not section:
        flash('Invalid section.', 'danger')
        return redirect(url_for('view.links', level=level))
    if current_user.is_authenticated and getattr(current_user, level + '_access') and section.level == level:
        form = SectionDetailsForm()

        if form.validate_on_submit():
            section.title = html_escape(form.title.data)
            section.description = html_escape(form.description.data)
            db.session.commit()
            return redirect(url_for('edit.edit_section', level=level, id=id))
        form.title.data = html_unescape(section.title)
        form.description.data = html_unescape(section.description) if section.description else ''
        return render_template('edit/edit-section-details.html.j2', level=level, title='Edit section | ' + level.capitalize(), form=form, id=id)
    flash('You are not authorised to edit sections for this level.', 'danger')
    return redirect(url_for('view.links', level=level))


@edit.route('/<string:level>/edit/links/<int:section_id>/link/new', methods=['GET', 'POST'])
@login_required
def new_link(level, section_id):
    section = Section.query.get(section_id)
    if not section:
        flash('Invalid section.', 'danger')
        return redirect(url_for('view.links', level=level))
    if current_user.is_authenticated and getattr(current_user, level + '_access') and section.level == level:
        form = LinkDetailsForm()
        if form.validate_on_submit():
            last_link = Link.query.filter_by(section_id=section_id).order_by(Link.order.desc()).first()
            order = last_link.order + 1 if last_link else 1
            link = Link(section_id=section_id, title=html_escape(form.title.data), url=form.link.data, order=order)
            db.session.add(link)
            db.session.commit()
            return redirect(url_for('edit.edit_section', level=level, id=section_id))
        return render_template('edit/new-link.html.j2', level=level, title='New link | ' + level.capitalize(), form=form, section=section)
    flash('You are not authorised to create links for this level.', 'danger')
    return redirect(url_for('view.links', level=level))


@edit.route('/<string:level>/edit/links/<int:section_id>/link/edit/<int:id>', methods=['GET', 'POST'])
def edit_link(level, section_id, id):
    section = Section.query.get(section_id)
    link = Link.query.get(id)
    if not section:
        flash('Invalid section.', 'danger')
        return redirect(url_for('view.links', level=level))
    if not link:
        flash('Invalid link.', 'danger')
        return redirect(url_for('edit.edit_section', level=level, id=section_id))
    if current_user.is_authenticated and getattr(current_user, level + '_access') and section.level == level and link.section_id == section.id:
        if not link.is_doc:
            form = LinkDetailsForm()
            if form.validate_on_submit():
                link.title = html_escape(form.title.data)
                link.url = form.link.data
                db.session.commit()
                return redirect(url_for('edit.edit_section', level=level, id=section_id))
            form.title.data = html_unescape(link.title)
            form.link.data = link.url
            return render_template('edit/edit-link.html.j2', level=level, title='Edit link | ' + level.capitalize(), form=form, section=section)
        else:
            file_error = None
            form = EditFileDetailsForm()

            if form.validate_on_submit():
                filename = secure_filename(form.file.data.filename)
                url = url_for('main.file', level=level, filename=filename)
                if os.path.exists(os.path.join(current_app.root_path, 'files', level, filename)) and url != link.url and form.file.data.filename:
                    file_error = 'A file with the same name already exists. Please rename the file and try uploading it again.'
                    return render_template('edit/edit-file.html.j2', level=level, title='Edit file | ' + level.capitalize(), form=form, section=section, file_error=file_error)
                link.title = html_escape(form.title.data)
                if filename:

                    old_url = unquote(link.url).split('/')
                    old_filename = ''.join(old_url[3:])
                    os.remove(os.path.join(current_app.root_path, 'files', level, old_filename))
                    form.file.data.save(os.path.join(current_app.root_path, 'files', level, filename))
                    link.url = url_for('main.file', level=level, filename=filename)

                db.session.commit()

                return redirect(url_for('edit.edit_section', level=level, id=section_id))
            form.title.data = html_unescape(link.title)
            return render_template('edit/edit-file.html.j2', level=level, title='New file | ' + level.capitalize(), form=form, section=section, file_error=file_error)
    flash('You are not authorised to edit links for this level.', 'danger')
    return redirect(url_for('view.links', level=level))


@edit.route('/<string:level>/edit/links/<int:section_id>/link/delete/<int:id>', methods=['GET', 'POST'])
def delete_link(level, section_id, id):
    section = Section.query.get(section_id)
    link = Link.query.get(id)
    if not section:
        flash('Invalid section.', 'danger')
        return redirect(url_for('view.links', level=level))
    if not link:
        flash('Invalid link.', 'danger')
        return redirect(url_for('edit.edit_section', level=level, id=section_id))
    if current_user.is_authenticated and getattr(current_user, level + '_access') and section.level == level and link.section_id == section.id:
        if link.is_doc:
            url = unquote(link.url).split('/')
            filename = ''.join(url[3:])
            os.remove(os.path.join(current_app.root_path, 'files', level, filename))
        db.session.delete(link)
        db.session.commit()
        return redirect(url_for('edit.edit_section', level=level, id=section_id))
    flash('You are not authorised to edit links for this level.', 'danger')
    return redirect(url_for('view.links', level=level))


@edit.route('/<string:level>/edit/links/<int:section_id>/file/new', methods=['GET', 'POST'])
@login_required
def new_file(level, section_id):
    section = Section.query.get(section_id)
    file_error = None
    if not section:
        flash('Invalid section.', 'danger')
        return redirect(url_for('view.links', level=level))
    if current_user.is_authenticated and getattr(current_user, level + '_access') and section.level == level:
        form = FileDetailsForm()
        if form.validate_on_submit():
            filename = secure_filename(form.file.data.filename)
            if os.path.exists(os.path.join(current_app.root_path, 'files', level, filename)):
                file_error = 'A file with the same name already exists. Please rename the file and try uploading it again.'
                return render_template('edit/new-file.html.j2', level=level, title='New file | ' + level.capitalize(), form=form, section=section, file_error=file_error)
            last_link = Link.query.filter_by(section_id=section_id).order_by(Link.order.desc()).first()
            order = last_link.order + 1 if last_link else 1
            link = Link(section_id=section_id, title=html_escape(form.title.data), url='', order=order, is_doc=True)
            db.session.add(link)
            db.session.commit()

            form.file.data.save(os.path.join(current_app.root_path, 'files', level, filename))

            link.url = url_for('main.file', level=level, filename=filename)
            db.session.commit()

            return redirect(url_for('edit.edit_section', level=level, id=section_id))
        return render_template('edit/new-file.html.j2', level=level, title='New file | ' + level.capitalize(), form=form, section=section, file_error=file_error)
    flash('You are not authorised to create links for this level.', 'danger')
    return redirect(url_for('view.links', level=level))


@edit.route('/<string:level>/edit/calendar/delete/<string:id>')
@login_required
def delete_event(level, id):
    event = Event.query.get(id)
    if not event:
        flash('Invalid section.', 'danger')
        return redirect(url_for('view.calendar', level=level))
    if current_user.is_authenticated and getattr(current_user, level + '_access') and event.level == level:
        return render_template('edit/delete-event.html.j2', level=level, title='Delete event | ' + level.capitalize(), event=event)
    flash('You are not authorised to delete events for this level.', 'danger')
    return redirect(url_for('view.calendar', level=level))


@edit.route('/<string:level>/edit/calendar/delete/<string:id>/confirm')
@login_required
def confirm_delete_event(level, id):
    event = Event.query.get(id)
    if not event:
        flash('Invalid section.', 'danger')
        return redirect(url_for('view.calendar', level=level))
    if current_user.is_authenticated and getattr(current_user, level + '_access') and event.level == level:
        db.session.delete(event)
        db.session.commit()
        return redirect(url_for('view.calendar', level=level))
    flash('You are not authorised to delete events for this level.', 'danger')
    return redirect(url_for('view.calendar', level=level))


@edit.route('/<string:level>/edit/calendar/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def event(level, id):
    event = Event.query.get(id)
    if not event:
        flash('Invalid event.', 'danger')
        return redirect(url_for('view.calendar', level=level))
    if current_user.is_authenticated and getattr(current_user, level + '_access') and event.level == level:
        form = EventForm()
        if form.validate_on_submit():
            event.title = html_escape(form.title.data)
            start_hour, start_minute = html_escape(form.start_time.data).split(':')
            event.start = datetime.datetime(form.start_date.data.year, form.start_date.data.month, form.start_date.data.day, int(start_hour), int(start_minute), 0)
            if form.end_time.data:
                end_hour, end_minute = html_escape(form.end_time.data).split(':')
                if form.end_date.data:
                    event.end = datetime.datetime(form.end_date.data.year, form.end_date.data.month, form.end_date.data.day, int(end_hour), int(end_minute), 0)
                else:
                    event.end = datetime.datetime(form.start_date.data.year, form.start_date.data.month, form.start_date.data.day, int(end_hour), int(end_minute), 0)
            else:
                event.end = None
            event.location = form.location.data
            event.description = form.description.data
            db.session.commit()
            return redirect(url_for('view.event', level=level, id=id))
        form.title.data = html_unescape(event.title)
        form.description.data = html_unescape(event.description)
        form.location.data = html_unescape(event.location)
        start = event.start
        form.start_date.data = datetime.date(start.year, start.month, start.day)
        form.start_time.data = start.strftime("%H:%M")
        end = event.end
        if end:
            form.end_date.data = datetime.date(end.year, end.month, end.day)
            form.end_time.data = end.strftime("%H:%M")
        return render_template('edit/event.html.j2', level=level, title='Edit Event | ' + level.capitalize(), form=form, new_event=False, id=id)
    flash('You are not authorised to edit events for this level.', 'danger')
    return redirect(url_for('view.event', level=level, id=id))


@edit.route('/<string:level>/edit/calendar/new', methods=['GET', 'POST'])
@login_required
def new_event(level):
    if current_user.is_authenticated and getattr(current_user, level + '_access'):
        form = EventForm()
        if form.validate_on_submit():
            title = html_escape(form.title.data)
            start_hour, start_minute = form.start_time.data.split(':')
            start = datetime.datetime(form.start_date.data.year, form.start_date.data.month, form.start_date.data.day, int(start_hour), int(start_minute), 0)
            if form.end_time.data:
                end_hour, end_minute = form.end_time.data.split(':')
                if form.end_date.data:
                    end = datetime.datetime(form.end_date.data.year, form.end_date.data.month, form.end_date.data.day, int(end_hour), int(end_minute), 0)
                else:
                    end = datetime.datetime(form.start_date.data.year, form.start_date.data.month, form.start_date.data.day, int(end_hour), int(end_minute), 0)
            else:
                end = None
            location = form.location.data
            description = form.description.data
            event = Event(title=title, start=start, end=end, location=location, description=description, level=level)
            db.session.add(event)
            db.session.commit()
            return redirect(url_for('view.event', level=level, id=event.id))
        return render_template('edit/event.html.j2', level=level, title='New Event | ' + level.capitalize(), form=form, new_event=True, id=None)
    flash('You are not authorised to create events for this level.', 'danger')
    return redirect(url_for('view.calendar', level=level))
