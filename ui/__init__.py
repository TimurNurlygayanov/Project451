from flask import Flask

import ui.config as cfg

app = Flask(__name__,
            template_folder=cfg.AppConfig['TEMPLATE_FOLDER'],
            static_folder=cfg.AppConfig['STATIC_FOLDER'])

app.secret_key = cfg.AppConfig['FORM_SECRET_KEY']

from ui import views
