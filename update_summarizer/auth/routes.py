import os

from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from flask_login import current_user, login_required
from flask_login import login_user as login_user_function
from flask_login import logout_user as logout_user_function
from jwt import encode

from update_summarizer import app, bcrypt, db
from update_summarizer.auth.forms import *
from update_summarizer.auth.utils import (email_verify_mail_body,
                                          generate_token,
                                          password_reset_key_mail_body)
from update_summarizer.mails import send_mail
from update_summarizer.models import Profile, Role, Subscription, User

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/register", methods=["GET", "POST"])
def register_user():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    form = RegisterForm()
    if form.validate_on_submit():
        # Generating token
        generated_token_for_email = generate_token(6)
        # Hashing
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        hashed_token = bcrypt.generate_password_hash(
            generated_token_for_email).decode("utf-8")
        # Creating user
        all_users = User.query.all()
        user = None
        if len(all_users) == 0:
            user = User(form.email.data, hashed_password,
                        hashed_token, Role.ADMIN)
        else:
            user = User(form.email.data, hashed_password,
                        hashed_token, Role.GENERAL)
        db.session.add(user)
        db.session.commit()
        # Creating profile
        profile = Profile(form.first_name.data, form.last_name.data, user.id, 2)
        db.session.add(profile)
        db.session.commit()
        subscription = Subscription(profile.id, None)
        db.session.add(subscription)
        db.session.commit()
        # Sending email
        send_mail(user.email, "Email Verification Code",
                  email_verify_mail_body(user.id, generated_token_for_email))
        fetched_user = User.query.filter_by(id=user.id).first()
        flash(
            f"Account created for {fetched_user.profile.first_name} {fetched_user.profile.last_name}. Check your email to continue.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form, active='register')


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        # Fetching the user
        fetched_user = User.query.filter_by(email=form.email.data).first()
        # Checking the email and password
        if fetched_user and bcrypt.check_password_hash(fetched_user.password, form.password.data):
            if not fetched_user.is_verified:
                flash("You need to verify your email address to login",
                      category="danger")
                return redirect(url_for("auth.login"))
            login_user_function(fetched_user, remember=form.remember_me.data)
            next_page = request.args.get("next")
            response = redirect(next_page) if next_page else redirect(
                url_for('main.homepage'))
            # jtw
            jwt_token = encode({
                "id": fetched_user.id,
                "email": fetched_user.email,
            }, app.config.get("JWT_SECRET_KEY"), algorithm="HS256")
            response.set_cookie("access_token", jwt_token, max_age=60*60*30)
            flash("Login Successfull.", "success")
            return response
        else:
            flash("Login Failed! Please Check Email and Password.", "danger")
    return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user_function()
    return redirect(url_for("auth.login"))


@auth.route("/verify-email/<int:id>/<string:token>")
def verify_email(id: int, token: str):
    user = User.query.filter_by(id=id).first()
    if not user:
        flash('User not found.', category='danger')
        return redirect(url_for('auth.login'))
    isMatched = bcrypt.check_password_hash(user.verified_code, token)
    if not isMatched:
        flash('Token did not matched.', category='danger')
    else:
        user.verified_code = None
        user.is_verified = True
        db.session.commit()
        flash('Your account is now verified.', category='success')
    return redirect(url_for('auth.login'))


@auth.route("/forget_password", methods=["GET", "POST"])
def forget_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    form = ForgetPasswordForm()
    if form.validate_on_submit():
        # Fetching the user
        user = User.query.filter_by(email=form.email.data).first()
        # Sending email
        send_mail(user.email, "Password Reset Token",
                  password_reset_key_mail_body(user.id, user.get_reset_token(), int(os.getenv("EXPIRE_TIME"))))
        flash(f"Check your email to continue.", "primary")
        return redirect(url_for('auth.login'))
    return render_template("auth/forget_password.html", form=form)


@auth.route("/reset_password/<int:id>/<string:token>", methods=["GET", "POST"])
def reset_password(id: int, token: str):
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    # Verifying the token
    veridication_result = User.verify_reset_key(
        id, token, int(os.getenv("EXPIRE_TIME")))
    if not veridication_result["is_authenticate"]:
        return render_template("main/errors.html", status=400, message=f"{veridication_result['message']}")
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user = User.query.get(id)
        user.password = hashed_password
        db.session.commit()
        flash(f"{veridication_result['message']}", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password.html", form=form)
