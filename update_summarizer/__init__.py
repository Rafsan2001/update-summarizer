import os

from datetime import datetime, timedelta

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from update_summarizer import auth

load_dotenv()

# Create and Configure the App
app = Flask(__name__)

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

from update_summarizer.auth.routes import auth
from update_summarizer.main.routes import main
from update_summarizer.profiles.routes import profiles
from update_summarizer.admin.routes import admin

@app.errorhandler(404) 
def invalid_route(e): 
    return render_template("main/errors.html", status=404, message="The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.")

# Registering blueprints
app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(profiles)
app.register_blueprint(admin)
