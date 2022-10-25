from email.policy import default
import enum
from datetime import datetime

from flask_login import UserMixin
from itsdangerous import TimedSerializer
from itsdangerous.exc import BadTimeSignature, SignatureExpired

from update_summarizer import app, db, login_manager


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# defining enum
class Role(enum.Enum):
    GENERAL = "general"
    MODERATOR = "moderator"
    ADMIN = "admin"


# Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    verified_code = db.Column(db.String)
    is_verified = db.Column(db.Boolean, default=False)
    role = db.Column(db.Enum(Role), nullable=False)
    profile = db.relationship("Profile", backref="user", uselist=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(
        self, email: str, password: str, verified_code: str, role: str
    ) -> None:
        self.email = email
        self.password = password
        self.verified_code = verified_code
        self.role = role

    def get_joindate(self):
        return self.created_at.strftime("%d %B, %Y")

    def get_reset_token(self):
        # https://stackoverflow.com/questions/46486062/the-dumps-method-of-itsdangerous-throws-a-typeerror
        serializer = TimedSerializer(app.config["SECRET_KEY"], "confirmation")
        return serializer.dumps(self.id)

    @staticmethod
    def verify_reset_key(id: int, token: str, max_age=1800):
        # 1800 seconds means 30 minutes
        serializer = TimedSerializer(app.config["SECRET_KEY"], "confirmation")
        try:
            result = serializer.loads(token, max_age=max_age)
        except SignatureExpired:
            return {
                "is_authenticate": False,
                "message": "Token is expired! Please re-generate the token.",
            }
        except BadTimeSignature:
            return {"is_authenticate": False, "message": "Token is not valid."}
        if result != id:
            return {
                "is_authenticate": False,
                "message": "Token is not valid for this user.",
            }
        return {"is_authenticate": True, "message": "Password successfully changed."}


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    profile_photo = db.Column(
        db.String, default="/images/default/default.png"
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    subscription = db.relationship(
        "Subscription", backref="profile", uselist=False)
    feedback = db.relationship("Feedback", backref="profile")
    rating = db.relationship("Rating", backref="profile")

    def __init__(
        self,
        first_name: str,
        last_name: str,
        user_id: int,
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = user_id

    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    text = db.Column(db.String(50), nullable=False)

    def __init__(
        self,
        text: str,
        profile_id: int,
    ) -> None:
        self.text = text
        self.profile_id = profile_id
    
    def get_created_at(self):
        return self.created_at.strftime("%d %B, %Y")

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    rating = db.Column(db.Integer, nullable=False)

    def __init__(
        self,
        rating: str,
        profile_id: int,
    ) -> None:
        self.rating = rating
        self.profile_id = profile_id

    def get_created_at(self):
        return self.created_at.strftime("%d %B, %Y")


class TrackSummary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    count = db.Column(db.Integer, default=1)

    def __init__(
        self,
        profile_id: int,
        count: int = 1,

    ) -> None:
        self.count = count
        self.profile_id = profile_id


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    exp_date = db.Column(db.DateTime)
    subscription_status = db.Column(db.String(15), default="free")

    def __init__(
        self,
        profile_id: int,
        exp_date,
        subscription_status: str = "free"

    ) -> None:
        self.exp_date = exp_date
        self.subscription_status = subscription_status
        self.profile_id = profile_id
