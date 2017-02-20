import os

basedir = os.path.abspath(os.path.dirname(__file__))

AppConfig = {
    'DEBUG_MODE': True,
    'HOST': os.getenv('HOST', '0.0.0.0'),
    'PORT': int(os.getenv('PORT', 5000)),
    'SECRET_KEY': os.urandom(32),
    'INDEX_GREETING': 'Hello! You\'re using RESTful API of Project451.<br>'
}

DatabaseConfig = {
    'SQLALCHEMY_DATABASE_URI': os.getenv('DATABASE_URI', 'Database URI')
}
