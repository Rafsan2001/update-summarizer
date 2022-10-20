import os
from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)

admin = Blueprint("admin", __name__)


@admin.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("admin/dashboard.html")
