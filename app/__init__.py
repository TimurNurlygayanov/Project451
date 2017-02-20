from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

import app.config as cfg

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = cfg.DatabaseConfig['SQLALCHEMY_DATABASE_URI']
login_manager = LoginManager(app)
db = SQLAlchemy(app)

from app import models
from app.api import views
