import os

basedir = os.path.abspath(os.path.dirname(__file__))

AppConfig = {
    'DEBUG_MODE': True,
    'HOST': os.getenv('HOST', '0.0.0.0'),
    'PORT': int(os.getenv('PORT', 5000)),
}
