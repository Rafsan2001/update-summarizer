import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_apscheduler import APScheduler
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from update_summarizer import auth

load_dotenv()

# Create and Configure the App
app = Flask(__name__)

scheduler = APScheduler()

# Secret Keys
app.secret_key = os.getenv("SECRET_KEY")

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_SERVER')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = "static/images/uploads"


app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = os.getenv("MAIL_PORT")
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")


# Database
db = SQLAlchemy(app)

# Migration
migrate = Migrate(app, db)

# Encryption
bcrypt = Bcrypt(app)

#Login-Manager
login_manager = LoginManager(app)

login_manager.login_view = "auth.login"
login_manager.login_message_category = "primary"


# Mail
mail = Mail(app)

import update_summarizer.models
from update_summarizer.admin.routes import admin
from update_summarizer.auth.routes import auth
from update_summarizer.checkout.routes import checkout
from update_summarizer.feedbacks.routes import feedbacks
from update_summarizer.main.routes import main
from update_summarizer.news.routes import news
from update_summarizer.profiles.routes import profiles


@app.errorhandler(404) 
def invalid_route(e): 
    return render_template("main/errors.html", status=404, message="The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.")

# Registering blueprints
app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(profiles)
app.register_blueprint(admin)
app.register_blueprint(feedbacks)
app.register_blueprint(news)
app.register_blueprint(checkout)

from update_summarizer.models import User


def job_check_expire_dates():
    date_format = '%d/%m/%Y'
    all_users = User.query.all()
    for user in all_users:
        sub = user.profile.subscription
        if sub.subscription_status != 'free':
            exp = datetime.strptime(sub.exp_date, date_format)
            now = datetime.strptime(datetime.utcnow(), date_format)
            
            if now > exp:
                # expired
                user.subscription.subscription_status = 'free'
                user.subscription.exp_date = None
                user.subscription.updated_at = datetime.utcnow()
                db.session.commit()

def job_add_summary_token():
    all_users = User.query.all()
    for user in all_users:
        sub = user.profile.subscription
        if sub.subscription_status == 'free':
            user.profile.summary_left = user.profile.summary_left + 1
        elif sub.subscription_status == 'silver':
            user.profile.summary_left = user.profile.summary_left + 5
        elif sub.subscription_status == 'gold':
            user.profile.summary_left = user.profile.summary_left + 7
        else:
            user.profile.summary_left = user.profile.summary_left + 10
