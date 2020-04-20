from flask import current_app
from flask_login import UserMixin
from jghsdofe import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(10), nullable=False)
    content = db.Column(db.Text, nullable=False)
    edited = db.Column(db.Boolean, nullable=False, default=False)
    date_posted = db.Column(db.DateTime, nullable=False)
    date_edited = db.Column(db.DateTime)
    starred = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"Announcement('{self.level}', '{self.content}')"


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(10), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Section('{self.level}', '{self.title}')"


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_doc = db.Column(db.Boolean, nullable=False, default=False)
    title = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    order = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Link('{self.section_id}', '{self.title}')"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    gold_access = db.Column(db.Boolean, nullable=False, default=False)
    silver_access = db.Column(db.Boolean, nullable=False, default=False)
    bronze_access = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"User('{self.username}')"


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(10), nullable=False)
    title = db.Column(db.String(32), nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime)
    location = db.Column(db.Text)
    description = db.Column(db.Text)
