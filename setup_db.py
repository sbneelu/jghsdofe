from jghsdofe import create_app, db
from jghsdofe.models import Announcement, Section, Link, Event, User
import datetime

app = create_app()


def setup_db(db, app):

    with app.app_context():
        db.create_all()

        db.session.commit()


setup_db(db, app)
