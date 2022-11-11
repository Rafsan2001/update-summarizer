import os
from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)

news = Blueprint("news", __name__)


@news.route("/english", methods=["GET"])
def english_news():
    return render_template("news/english/english-news.html")

@news.route("/international", methods=["GET"])
def international_english():
    return render_template("news/english/international.html")

@news.route("/politics", methods=["GET"])
def politics_english():
    return render_template("news/english/politics.html")

@news.route("/entertainments", methods=["GET"])
def entertainments_english():
    return render_template("news/english/entertainments.html")

@news.route("/buisness", methods=["GET"])
def buisness_english():
    return render_template("news/english/buisness.html")

@news.route("/sports", methods=["GET"])
def sports_english():
    return render_template("news/english/sports.html")

@news.route("/details", methods=["GET"])
def details():
    return render_template("news/english/details.html")




@news.route("/বাংলা", methods=["GET"])
def bangla_news():
    return render_template("news/bangla/bangla-news.html")

@news.route("/আন্তর্জাতিক", methods=["GET"])
def international_bangla():
    return render_template("news/bangla/international.html")

@news.route("/রাজনীতি", methods=["GET"])
def politics_bangla():
    return render_template("news/bangla/politics.html")

@news.route("/বিনোদন", methods=["GET"])
def entertainments_bangla():
    return render_template("news/bangla/entertainments.html")

@news.route("/ব্যবসা", methods=["GET"])
def buisness_bangla():
    return render_template("news/bangla/buisness.html")

@news.route("/খেলাধুলা", methods=["GET"])
def sports_bangla():
    return render_template("news/bangla/sports.html")

@news.route("/bangla-details", methods=["GET"])
def bangla_details():
    return render_template("news/bangla/details.html")