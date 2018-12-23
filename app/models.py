import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class Meditation(db.Model):
    __tablename__ = "meditations"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    youtube_id = db.Column(db.String(128))

    def __repr__(self):
        return '<Meditation: Youtube ID: {}>'.format(self.youtube_id)


user_daily_meditation = db.Table('association',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('daily_meditation_id', db.Integer, db.ForeignKey('daily_meditations.id'))
)


class DailyMeditation(db.Model):
    __tablename__ = "daily_meditations"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True)

    meditation_id = db.Column(db.Integer, db.ForeignKey('meditations.id'))
    meditation = db.relationship('Meditation')

    users = db.relationship(
        "User",
        secondary=user_daily_meditation,
        back_populates="daily_meditations"
    )

    def __repr__(self):
        return "<Daily Meditation date: {} meditation: {}>".format(self.date, self.meditation.title)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))

    daily_meditations = db.relationship("DailyMeditation", backref="user", lazy="dynamic")

    daily_meditations = db.relationship(
        "DailyMeditation",
        secondary=user_daily_meditation,
        back_populates="users"
    )

    def __repr__(self):
        return "<User id: {} email: {}>".format(self.id, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))