from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, DateField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

from app.models import Meditation, User


class CreateMeditationForm(FlaskForm):
    youtube_id = StringField('Youtube ID', validators=[DataRequired()])
    title = StringField('Meditation Title', validators=[DataRequired()])
    submit_meditation = SubmitField('Add Meditation')

    def validate_youtube_id(self, youtube_id):
        meditation = Meditation.query.filter_by(youtube_id=youtube_id.data).first()
        if meditation is not None:
            raise ValidationError('Meditation is already added.')


class FriendForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit_friend = SubmitField('Add User')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('No user with that username.')