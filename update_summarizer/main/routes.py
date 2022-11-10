import os
from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def homepage():
    return render_template("main/homepage.html")

@main.route("/premium", methods=["GET"])
def premium():
    return render_template("main/premium.html")

@main.route("/subscription-pack", methods=["GET"])
def subscription_pack():
    return render_template("main/subscription_pack.html")

@main.route("/about-us", methods=["GET"])
def about_us():
    return render_template("main/about_us.html")

@main.route("/help", methods=["GET"])
def help():
    return render_template("main/help.html")

@main.route("/summary-generate", methods=["GET"])
def summarizer():
    return render_template("main/homepage.html")