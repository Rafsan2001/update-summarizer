from flask import Blueprint, render_template, flash, url_for, redirect
from flask_login import current_user, login_required
from update_summarizer import db

from flask import Blueprint, render_template

from update_summarizer.profiles.form import *
from update_summarizer.profiles.utils import remove_photo, save_photos


profiles = Blueprint("profiles", __name__, url_prefix="/profiles")


@profiles.route("/", methods=["GET", "POST"])
@login_required
def view_profile():
    form = ProfileInfoForm()
    if form.validate_on_submit():
        current_user.profile.first_name = form.first_name.data
        current_user.profile.last_name = form.last_name.data
        if form.profile_photo.data:
            file_path = current_user.profile.profile_photo
            if not ("/images/default/ProfilePhotos/default.png" in file_path):
                remove_photo(file_path)
            photo_file = save_photos(
                form.profile_photo.data, current_user.id, "profile", 250, 250)
            current_user.profile.profile_photo = "/images/uploads/profile/" + photo_file
        db.session.commit()
        return render_template("profiles/view_profile.html", form=form)
    form.first_name.data = current_user.profile.first_name
    form.last_name.data = current_user.profile.last_name
    return render_template("profiles/view_profile.html", form=form)

@profiles.route("/remove-profile-photo")
@login_required
def remove_profile_photo():
    if not ("/images/default/ProfilePhotos/default.png" in current_user.profile.profile_photo):
        remove_photo(current_user.profile.profile_photo)
        current_user.profile.profile_photo = "/images/default/ProfilePhotos/default.png"
        db.session.commit()
        flash("Profile photo removed.", "success")
    else:
        flash("Cannot remove default profile photo.", "danger")
    return redirect(url_for("profiles.view_profile"))

@profiles.route("/my-plan", methods=["GET", "POST"])
def my_plan():
    return render_template("profiles/my_plan.html")
