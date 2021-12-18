import os
from flask import Flask
from flask_gravatar import Gravatar
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import stripe


app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///leb-shop-app.db")
app.config["STRIPE_PUBLIC_KEY"] = os.environ.get("STRIPE_PUBLIC_KEY")
app.config["STRIPE_SECRET_KEY"] = os.environ.get("STRIPE_SECRET_KEY")

db = SQLAlchemy(app)
login_manager = LoginManager(app)
Bootstrap(app)

login_manager.login_view = "login"
login_manager.login_message = "Please log in first to make purchase or add items to cart."
login_manager.login_message_category = "info"

stripe.api_key = app.config["STRIPE_SECRET_KEY"]

# -------------------------------------- #
from lebshop import routes