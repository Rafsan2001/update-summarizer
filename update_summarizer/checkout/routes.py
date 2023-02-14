import os
from datetime import datetime

import stripe
from dateutil.relativedelta import relativedelta
from flask import Blueprint, flash, redirect, request, url_for
from flask_login import current_user, login_required

from update_summarizer import app, bcrypt, db
from update_summarizer.models import Profile

checkout = Blueprint("checkout", __name__, url_prefix="/checkout")

DOMAIN = f'http://localhost:{os.getenv("PORT")}/checkout'

stripe.api_key = os.getenv('STRIPE_KEY')

@login_required
@checkout.route('/silver', methods=['POST'])
def create_checkout_session_silver():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items = [
                {
                    'price': os.getenv('SILVER_PRICE_KEY'),
                    'quantity': 1
                }
            ],
            mode='subscription',
            success_url=f'{DOMAIN}/success?id={current_user.profile.id}&mode=silver',
            cancel_url=f'{DOMAIN}/cancel',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

@login_required
@checkout.route('/gold', methods=['POST'])
def create_checkout_session_gold():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items = [
                {
                    'price': os.getenv('GOLD_PRICE_KEY'),
                    'quantity': 1
                }
            ],
            mode='subscription',
            success_url=f'{DOMAIN}/success?id={current_user.profile.id}&mode=gold',
            cancel_url=f'{DOMAIN}/cancel',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

@login_required
@checkout.route('/platinum', methods=['POST'])
def create_checkout_session_platinum():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items = [
                {
                    'price': os.getenv('PLATINUM_PRICE_KEY'),
                    'quantity': 1
                }
            ],
            mode='subscription',
            success_url=f'{DOMAIN}/success?id={current_user.profile.id}&mode=platinum',
            cancel_url=f'{DOMAIN}/cancel',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

@login_required
@checkout.route('/success', methods=['GET'])
def success():
    profile_id = request.args.get('id')
    mode = request.args.get('mode')

    duration = 1
    summary_left = 5

    if mode == 'gold':
        duration = 3
        summary_left = 7
    elif mode == 'platinum':
        duration = 6
        summary_left = 10

    profile = Profile.query.filter_by(id=profile_id).first()
    subscription = profile.subscription

    date_format = '%d/%m/%Y'

    now = datetime.strptime(datetime.today().strftime(date_format), date_format)
    expire_date = (now + relativedelta(months=duration)).date()

    subscription.subscription_status = mode
    subscription.exp_date = expire_date
    subscription.updated_at = datetime.utcnow()

    profile.summary_left = profile.summary_left + summary_left

    db.session.commit()
    flash(f'{mode.capitalize()} subscribed', 'success')
    return redirect(url_for('main.subscription_pack'))
    
@login_required
@checkout.route('/cancel', methods=['GET'])
def cancel():
    return redirect(url_for('main.subscription_pack'))

