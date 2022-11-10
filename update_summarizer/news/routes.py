import os
from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)

news = Blueprint("news", __name__)


@news.route("/bangladesh", methods=["GET"])
def bangladesh():
    return render_template("news/bangladesh.html")

@news.route("/details", methods=["GET"])
def details():
    return render_template("news/details.html")