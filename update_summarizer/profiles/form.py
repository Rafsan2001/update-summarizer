from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from update_summarizer import bcrypt
from update_summarizer.models import User
from wtforms import (DateField, PasswordField, StringField, SubmitField,
                     TextAreaField)
from wtforms.validators import (URL, DataRequired, EqualTo, Length, Optional,
                                ValidationError)


class ProfileInfoForm(FlaskForm):
    profile_photo = FileField("Profile Photo", validators=[
                              FileAllowed(["jpg", "jpeg", "png"])])
    first_name = StringField("First Name", validators=[
        DataRequired(), Length(max=15, min=2)
    ], render_kw={"placeholder": "ex. Alen"})
    last_name = StringField("Last Name", validators=[
        DataRequired(), Length(max=15, min=2)
    ], render_kw={"placeholder": "ex. Walker"})
    save = SubmitField("Update")



# class ChangePasswordForm(FlaskForm):
#     old_password = PasswordField("Old Password", validators=[
#         DataRequired(), Length(min=6)
#     ], render_kw={"placeholder": "Type your old password"})

#     new_password = PasswordField("New Password", validators=[
#         DataRequired(), Length(min=6)
#     ], render_kw={"placeholder": "Type a new password"})

#     c_password = PasswordField("Confirm Password", validators=[
#         DataRequired(), Length(min=6), EqualTo(
#             "new_password", "Confirm password did not matched")
#     ], render_kw={"placeholder": "Retype the password"})

#     save = SubmitField("Update")

#     def validate_old_password(self, old_password):
#         user = User.query.get(current_user.id)
#         if not bcrypt.check_password_hash(user.password, old_password.data):
#             raise ValidationError("Password did not matched.")
