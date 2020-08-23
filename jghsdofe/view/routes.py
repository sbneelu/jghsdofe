from flask import abort, render_template, url_for, redirect, flash, request, Blueprint
from flask_login import login_user, logout_user, current_user, login_required
from jghsdofe.models import Announcement, Section, Link, Event
import datetime, json

view = Blueprint('view', __name__)

@view.route('/bronze')
def bronze():
    return redirect(url_for('view.summary', level='bronze'))

@view.route('/silver')
def silver():
    return redirect(url_for('view.summary', level='silver'))

@view.route('/gold')
def gold():
    return redirect(url_for('view.summary', level='gold'))

@view.route('/<string:level>/home')
def summary(level):
    if level not in ['bronze', 'silver', 'gold']:
        abort(404)
    starred_announcements = Announcement.query.filter(Announcement.level == level, Announcement.starred == True).all()
    unstarred_announcements = Announcement.query.filter(Announcement.level == level, Announcement.starred == False, Announcement.date_edited >= datetime.datetime.utcnow() - datetime.timedelta(days=8)).all()
    starred_announcements.sort(key=lambda a: a.date_edited, reverse=True)
    unstarred_announcements.sort(key=lambda a: a.date_edited, reverse=True)

    events = Event.query.filter(Event.level == level, Event.start <= datetime.datetime.utcnow() + datetime.timedelta(days=8), Event.start >= datetime.datetime.utcnow()).all()
    events_before = Event.query.filter(Event.level == level, Event.start <= datetime.datetime.utcnow(), Event.end >= datetime.datetime.utcnow()).all()

    for event in events_before:
        if event not in events:
            events.append(event)

    events.sort(key=lambda a: a.start)

    if current_user.is_authenticated and getattr(current_user, level + '_access'):
        return render_template('edit/level.html.j2', starred_announcements=starred_announcements, unstarred_announcements=unstarred_announcements, title=level.capitalize(), level=level, events=events)

    return render_template('view/level.html.j2', starred_announcements=starred_announcements, unstarred_announcements=unstarred_announcements, title=level.capitalize(), level=level, events=events)

@view.route('/<string:level>/announcements')
def announcements(level):
    if level not in ['bronze', 'silver', 'gold']:
        abort(404)
    starred_announcements = Announcement.query.filter(Announcement.level == level, Announcement.starred == True).all()
    unstarred_announcements = Announcement.query.filter(Announcement.level == level, Announcement.starred == False).all()
    starred_announcements.sort(key=lambda a: a.date_edited, reverse=True)
    unstarred_announcements.sort(key=lambda a: a.date_edited, reverse=True)

    if current_user.is_authenticated and getattr(current_user, level + '_access'):
        return render_template('edit/announcements.html.j2', starred_announcements=starred_announcements, unstarred_announcements=unstarred_announcements, title='Announcements | ' + level.capitalize(), level=level)

    return render_template('view/announcements.html.j2', starred_announcements=starred_announcements, unstarred_announcements=unstarred_announcements, title='Announcements | ' + level.capitalize(), level=level)


@view.route('/<string:level>/links')
def links(level):
    if level not in ['bronze', 'silver', 'gold']:
        abort(404)

    sections = Section.query.filter(Section.level == level).all()
    sections.sort(key=lambda s: s.order)

    section_ids = [section.id for section in sections]

    links = Link.query.filter(Link.section_id.in_(section_ids)).all()
    links.sort(key=lambda l: l.order)

    links_sorted = {}

    for section in sections:
        links_sorted[section.id] = []

    for link in links:
        links_sorted[link.section_id].append(link)

    if current_user.is_authenticated and getattr(current_user, level + '_access'):
        return render_template('edit/links.html.j2', title='Links and Documents | ' + level.capitalize(), level=level, sections=sections, links_sorted=links_sorted)

    return render_template('view/links.html.j2', title='Links and Documents | ' + level.capitalize(), level=level, sections=sections, links_sorted=links_sorted)


@view.route('/<string:level>/calendar')
def calendar(level):
    if level not in ['bronze', 'silver', 'gold']:
        abort(404)

    events_from_db = Event.query.filter(Event.level == level).all()
    events = []

    for ev in events_from_db:
        event = {
            "id": str(ev.id),
            "title": ev.title,
            "backgroundColor": "#a81e14",
            "borderColor": "#a81e14",
            "start": ev.start.strftime("%Y-%m-%dT%H:%M:%S"),
            "extendedProps": {}
        }

        if ev.end:
            event['end'] = ev.end.strftime("%Y-%m-%dT%H:%M:%S")

        if ev.description:
            event['extendedProps']['description'] = ev.description

        if ev.location:
            event['extendedProps']['location'] = ev.location

        events.append(event)

    events = json.dumps(events)

    if current_user.is_authenticated and getattr(current_user, level + '_access'):
        return render_template('edit/calendar.html.j2', title='Calendar | ' + level.capitalize(), level=level, events=events)

    return render_template('view/calendar.html.j2', title='Calendar | ' + level.capitalize(), level=level, events=events)


@view.route('/<string:level>/calendar/<int:id>')
def event(level, id):
    if level not in ['bronze', 'silver', 'gold']:
        abort(404)
    event = Event.query.get(id)
    if not event:
        flash('Invalid event.', 'danger')
        return redirect(url_for('view.calendar', level=level))
    authenticated = False
    if current_user.is_authenticated and getattr(current_user, level + '_access') and event.level == level:
        authenticated = True
    return render_template('view/event.html.j2', level=level, title='Event | ' + level.capitalize(), event=event, authenticated=authenticated)
