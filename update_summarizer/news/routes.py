import os
from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)

news = Blueprint("news", __name__)


@news.route("/english", methods=["GET"])
def english_news():
    return render_template("news/english/english-news.html")

@news.route("/details", methods=["GET"])
def english_details():
    return render_template("news/english/details.html")

@news.route("/details-2", methods=["GET"])
def english_details_2():
    return render_template("news/english/details-2.html")

@news.route("/international", methods=["GET"])
def international_english():
    return render_template("news/english/international.html")

@news.route("/sports_i_1", methods=["GET"])
def international_english_i_1():
    return render_template("news/english/details-i-1.html")

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

@news.route("/sports_s_1", methods=["GET"])
def sports_english_s_1():
    return render_template("news/english/details-s-1.html")






@news.route("/বাংলা", methods=["GET"])
def bangla_news():
    return render_template("news/bangla/bangla-news.html")

@news.route("/bangla-details", methods=["GET"])
def bangla_details():
    return render_template("news/bangla/details.html")

@news.route("/bangla-details2", methods=["GET"])
def bangla_details2():
    return render_template("news/bangla/details2.html")

@news.route("/আন্তর্জাতিক", methods=["GET"])
def international_bangla():
    return render_template("news/bangla/international.html")

@news.route("/bangla-details-int-1", methods=["GET"])
def bangla_details_int_1():
    return render_template("news/bangla/details-int-1.html")

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

@news.route("/bangla-details-s-1", methods=["GET"])
def bangla_details_s_1():
    return render_template("news/bangla/details-s-1.html")

