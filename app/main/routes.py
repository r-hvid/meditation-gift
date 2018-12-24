from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.main.forms import CreateMeditationForm, FriendForm
from app.models import User, Meditation, DailyMeditation
from datetime import date
from sqlalchemy.sql.expression import func


@bp.route('/', methods=['GET'])
def landing():
    return redirect(url_for('main.dashboard'))


@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    meditation_form = CreateMeditationForm()
    friend_form = FriendForm()

    stats = {
        'streak': current_user.streak,
        'total_meditations': current_user.daily_meditations.count()
    }

    if meditation_form.submit_meditation.data and meditation_form.validate_on_submit():
        new_meditation = Meditation(
            youtube_id=meditation_form.youtube_id.data,
            title=meditation_form.title.data
        )

        db.session.add(new_meditation)
        db.session.commit()
        flash("{} was added".format(new_meditation.title))
        return redirect(url_for('main.dashboard'))

    if friend_form.submit_friend.data and friend_form.validate_on_submit():
        friend = User.query.filter_by(username=friend_form.username.data).first()
        if friend:
            current_user.follow(friend)
            db.session.commit()
            flash("{} was added to your friend list".format(friend.username))
        return redirect(url_for('main.dashboard'))

    return render_template('dashboard.html', 
                            meditation_form=meditation_form,
                            friend_form=friend_form,
                            stats=stats)

@bp.route('/meditate', methods=['GET'])
@login_required
def meditate():
    daily_meditation = DailyMeditation.query.filter_by(date=date.today()).first()

    # If no meditations has been picked for the day pick a new one:
    if daily_meditation is None:
        random_meditation = Meditation.query.order_by(func.random()).first()

        daily_meditation = DailyMeditation(
            date=date.today(),
            meditation=random_meditation
        )

        db.session.add(daily_meditation)
        db.session.commit()

    return render_template('meditate.html', meditation=daily_meditation)


@bp.route('/meditate', methods=['POST'])
@login_required
def register_meditation():
    try:
        data = request.get_json()
        daily_meditation_id = data['daily_meditation_id']

        daily_meditation = DailyMeditation.query.get_or_404(daily_meditation_id)

        if daily_meditation in current_user.daily_meditations:
            flash("Good job. You meditated more than once today!")
        else:
            current_user.daily_meditations.append(daily_meditation)

            if current_user.is_streak():
                current_user.streak += 1
            else:
                current_user.streak = 1

            db.session.commit()
            flash("Congrats on completing today's meditation!")
    except KeyError:
        return jsonify({
            'status': 'fail'
        })

    return jsonify({
        'status': 'success'
    })