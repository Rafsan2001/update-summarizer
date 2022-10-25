from flask import (Blueprint, flash, redirect,
                   render_template, request, session, url_for)
from flask_login import login_required, current_user
from update_summarizer.models import Feedback, Rating
from update_summarizer import db

feedbacks = Blueprint("feedbacks", __name__)


@feedbacks.route('/feedback', methods=['POST'])
@login_required
def feedback():
    details = request.form.get('feedback-details')
    next_page = request.args.get("next")
    response = redirect(next_page) if next_page else redirect(
        url_for('main.homepage'))
    if not details and len(details) == 0:
        flash('You cannot submit an empty feedback', category='danger')
        return response
    feedback_model = Feedback(details, current_user.profile.id)
    db.session.add(feedback_model)
    db.session.commit()

    flash('Feedback added', category='success')
    return response


@feedbacks.route('/rating', methods=['POST'])
@login_required
def rating():
    rating1 = request.form.get('radio-1')
    rating2 = request.form.get('radio-2')
    rating3 = request.form.get('radio-3')
    rating4 = request.form.get('radio-4')
    rating5 = request.form.get('radio-5')

    next_page = request.args.get("next")
    response = redirect(next_page) if next_page else redirect(
        url_for('main.homepage'))

    if not rating1 and not rating2 and not rating3 and not rating4 and not rating5:
        flash('Validation error', category='danger')
        return response

    rate = 0
    if rating5:
        rate = 5
    elif rating4:
        rate = 4
    elif rating3:
        rate = 3
    elif rating2:
        rate = 2
    else:
        rate = 1

    rating_model = Rating(rate, current_user.profile.id)

    db.session.add(rating_model)
    db.session.commit()

    flash('Rating added', category='success')
    return response
