import os
from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from flask_login import login_required, current_user
from update_summarizer.models import Feedback, Rating, Role
admin = Blueprint("admin", __name__)


@admin.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    if current_user.role != Role.ADMIN:
        next_page = request.args.get("next")
        response = redirect(next_page) if next_page else redirect(
            url_for('main.homepage'))
        return response
    feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()[:4]
    ratings = Rating.query.order_by(Rating.created_at.desc()).all()[:6]
    return render_template("admin/dashboard.html", len=len, feedbacks=feedbacks, ratings=ratings)
