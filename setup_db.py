from jghsdofe import create_app, db
from jghsdofe.models import Announcement, Section, Link, Event, User
import datetime

app = create_app()


def setup_db(db, app):

    with app.app_context():
        db.create_all()

        db.session.add(User(username='gold_admin', password='$2b$12$4/.PZRDfMFxu6jnDPm9pMuok2pAWUz4l1/AAtMmHdsgjLXrLhwIG.', gold_access=True))
        db.session.add(User(username='silver_admin', password='$2b$12$4/.PZRDfMFxu6jnDPm9pMuok2pAWUz4l1/AAtMmHdsgjLXrLhwIG.', silver_access=True))
        db.session.add(User(username='bronze_admin', password='$2b$12$4/.PZRDfMFxu6jnDPm9pMuok2pAWUz4l1/AAtMmHdsgjLXrLhwIG.', bronze_access=True))
        db.session.add(User(username='gs_admin', password='$2b$12$4/.PZRDfMFxu6jnDPm9pMuok2pAWUz4l1/AAtMmHdsgjLXrLhwIG.', gold_access=True, silver_access=True))

        db.session.add(Announcement(level='gold', content='Test 1', date_posted=datetime.datetime.utcnow(), date_edited=datetime.datetime.utcnow()))
        db.session.add(Announcement(level='gold', content='Test 2', date_posted=datetime.datetime(2020, 3, 12, 1, 33, 23), edited=True, date_edited=datetime.datetime(2020, 3, 18, 14, 21, 23)))
        db.session.add(Announcement(level='gold', content='Test 3', date_posted=datetime.datetime(2020, 4, 10, 2, 31, 23), starred=True, date_edited=datetime.datetime(2020, 4, 10, 2, 31, 23)))
        db.session.add(Announcement(level='gold', content='Test 4', date_posted=datetime.datetime(2020, 3, 6, 5, 33, 23), edited=False, date_edited=datetime.datetime(2020, 3, 6, 5, 33, 23)))
        db.session.add(Announcement(level='gold', content='Test 5', date_posted=datetime.datetime(2020, 3, 12, 1, 33, 23), edited=True, date_edited=datetime.datetime(2020, 4, 6, 14, 21, 23)))
        db.session.add(Announcement(level='gold', content='Test 6', date_posted=datetime.datetime(2020, 2, 10, 2, 31, 23), edited=True, starred=True, date_edited=datetime.datetime(2020, 2, 15, 2, 31, 23)))

        db.session.add(Section(level='gold', title='Test Section 1', order=1))
        db.session.add(Section(level='gold', title='Test Section 2', description='Test description', order=2))
        db.session.add(Section(level='gold', title='Test Section 4', order=4))
        db.session.add(Section(level='gold', title='Test Section 3', description='Test description', order=3))
        db.session.add(Section(level='gold', title='Test Section 5', description='Test description', order=5))
        db.session.add(Section(level='gold', title='Test Section 6', description='Test description', order=6))
        db.session.add(Section(level='gold', title='Test Section 7', description='Test description', order=7))
        db.session.add(Section(level='gold', title='Test Section 8', description='Test description', order=8))

        db.session.add(Link(is_doc=False, title='S1 Link 1', url='https://www.google.com/?q=11', section_id=1, order=1))
        db.session.add(Link(is_doc=False, title='S1 Link 2', url='https://www.google.com/?q=12', section_id=1, order=2))
        db.session.add(Link(is_doc=False, title='S2 Link 1', url='https://www.google.com/?q=21', section_id=2, order=1))
        db.session.add(Link(is_doc=False, title='S1 Link 3', url='https://www.google.com/?q=13', section_id=1, order=3))
        db.session.add(Link(is_doc=False, title='S2 Link 2', url='https://www.google.com/?q=22', section_id=2, order=2))
        db.session.add(Link(is_doc=False, title='S2 Link 1', url='https://www.google.com/?q=21', section_id=4, order=1))
        db.session.add(Link(is_doc=False, title='S1 Link 3', url='https://www.google.com/?q=13', section_id=4, order=3))
        db.session.add(Link(is_doc=False, title='S2 Link 2', url='https://www.google.com/?q=22', section_id=4, order=2))

        db.session.add(Event(level='gold', title='Test Event 1', start=datetime.datetime(2020, 4, 10, 14, 30, 0), description='Description 1'))
        db.session.add(Event(level='gold', title='Test Event 2', start=datetime.datetime(2020, 4, 12, 10, 0, 0), end=datetime.datetime(2020, 4, 12, 12, 00, 0)))
        db.session.add(Event(level='gold', title='Test Event 3', start=datetime.datetime(2020, 4, 12, 10, 0, 0), end=datetime.datetime(2020, 4, 12, 12, 00, 0), location='Location 3'))
        db.session.add(Event(level='gold', title='Test Event 4', start=datetime.datetime(2020, 4, 8, 12, 0, 0), end=datetime.datetime(2020, 4, 10, 17, 30, 0), location='Location'))
        db.session.add(Event(level='gold', title='Test Event 5', start=datetime.datetime(2020, 4, 18, 23, 40, 0), location='Location'))
        db.session.add(Event(level='gold', title='Test Event 6', start=datetime.datetime(2020, 4, 22, 12, 0, 0), location='Location'))
        db.session.add(Event(level='gold', title='Test Event 7', start=datetime.datetime(2020, 4, 17, 12, 0, 0), end=datetime.datetime(2020, 4, 19, 17, 30, 0), description='Description'))
        db.session.add(Event(level='gold', title='Test Event 7', start=datetime.datetime(2020, 4, 12, 12, 0, 0), end=datetime.datetime(2020, 4, 18, 17, 30, 0), description='Description'))


        db.session.commit()


setup_db(db, app)
