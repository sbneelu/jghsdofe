from flask import abort, render_template, url_for, redirect, flash, request, Blueprint, current_app
from flask_login import current_user, login_required
from jghsdofe.models import Announcement, Section, Link
from jghsdofe import db
from jghsdofe.edit.forms import AnnouncementForm, SectionDetailsForm, LinkDetailsForm, FileDetailsForm, EditFileDetailsForm
import datetime
import os
from werkzeug import secure_filename
from urllib.parse import unquote


edit = Blueprint('edit', __name__)

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
    announcement = Announcement.query.get(id)
    if not announcement:
        flash('Invalid Announcement.', 'danger')
        return redirect(url_for('view.announcements', level=level))
    if current_user.is_authenticated and getattr(current_user, level + '_access') and announcement.level == level:
        form = AnnouncementForm()

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


@edit.route('/<string:level>/edit/links/new/section', methods=['GET', 'POST'])
@login_required
def new_section(level):
    if current_user.is_authenticated and getattr(current_user, level + '_access'):
        form = SectionDetailsForm()
        if form.validate_on_submit():
            section = Section(level=level, title=form.title.data, description=form.description.data, order=5)
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
            section.title = form.title.data
            section.description = form.description.data
            db.session.commit()
            return redirect(url_for('edit.edit_section', level=level, id=id))
        form.title.data = section.title
        form.description.data = section.description if section.description else ''
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
            link = Link(section_id=section_id, title=form.title.data, url=form.link.data, order=5)
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
                link.title = form.title.data
                link.url = form.link.data
                db.session.commit()
                return redirect(url_for('edit.edit_section', level=level, id=section_id))
            form.title.data = link.title
            form.link.data = link.url
            return render_template('edit/edit-link.html.j2', level=level, title='Edit link | ' + level.capitalize(), form=form, section=section)
        else:
            file_error = None
            form = EditFileDetailsForm()

            if form.validate_on_submit():
                filename = form.file.data.filename
                url = url_for('main.file', filename=level + '/' + filename)
                if os.path.exists(os.path.join(current_app.root_path, 'files', level, filename)) and url != link.url and form.file.data.filename:
                    file_error = 'A file with the same name already exists. Please rename the file and try uploading it again.'
                    return render_template('edit/edit-file.html.j2', level=level, title='Edit file | ' + level.capitalize(), form=form, section=section, file_error=file_error)
                link.title = form.title.data
                if form.file.data.filename:

                    old_url = unquote(link.url).split('/')
                    old_filename = ''.join(old_url[3:])
                    os.remove(os.path.join(current_app.root_path, 'files', level, old_filename))
                    form.file.data.save(os.path.join(current_app.root_path, 'files', level, filename))
                    link.url = url_for('main.file', filename=level + '/' + filename)

                db.session.commit()

                return redirect(url_for('edit.edit_section', level=level, id=section_id))
            form.title.data = link.title
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
            filename = form.file.data.filename
            if os.path.exists(os.path.join(current_app.root_path, 'files', level, filename)):
                file_error = 'A file with the same name already exists. Please rename the file and try uploading it again.'
                return render_template('edit/new-file.html.j2', level=level, title='New file | ' + level.capitalize(), form=form, section=section, file_error=file_error)
            link = Link(section_id=section_id, title=form.title.data, url='', order=5, is_doc=True)
            db.session.add(link)
            db.session.commit()

            form.file.data.save(os.path.join(current_app.root_path, 'files', level, filename))

            link.url = url_for('main.file', filename=level + '/' + filename)
            db.session.commit()

            return redirect(url_for('edit.edit_section', level=level, id=section_id))
        return render_template('edit/new-file.html.j2', level=level, title='New file | ' + level.capitalize(), form=form, section=section, file_error=file_error)
    flash('You are not authorised to create links for this level.', 'danger')
    return redirect(url_for('view.links', level=level))
