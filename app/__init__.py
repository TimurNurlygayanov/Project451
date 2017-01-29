from flask import Flask
from flask_login import LoginManager

import config as cfg


app = Flask(__name__)

login_manager = LoginManager(app)


from app import views, models
