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
    date = db.Column(db.Date, index=True, unique=True)

    meditation_id = db.Column(db.Integer, db.ForeignKey('meditations.id'))
    meditation = db.relationship('Meditation')

    users = db.relationship(
        "User",
        secondary=user_daily_meditation,
        back_populates="daily_meditations"
    )

    def __repr__(self):
        return "<Daily Meditation date: {} meditation: {}>".format(self.date, self.meditation.title)


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    streak = db.Column(db.Integer, default=0)

    daily_meditations = db.relationship("DailyMeditation", backref="user", lazy="dynamic")

    daily_meditations = db.relationship(
        "DailyMeditation",
        secondary=user_daily_meditation,
        back_populates="users",
        lazy="dynamic"
    )

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
    )

    def __repr__(self):
        return "<User id: {} email: {}>".format(self.id, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_streak(self):
        yesterday = datetime.date.today()-datetime.timedelta(days=1)
        yesterdays_meditation = DailyMeditation.query.filter_by(date=yesterday)

        if yesterdays_meditation in self.daily_meditations:
            return True

        return False

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def get_highscore(self):
        friends = [friend for friend in self.followed]
        friends.append(self)
        friends.sort(key=lambda current_friend: current_friend.streak, reverse=True)

        return friends


@login.user_loader
def load_user(id):
    return User.query.get(int(id))