from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from app import db, cfg
from app.api.helper import hash_password


USER_ROLES = {
    'user': 0,
    'manager': 1,
    'admin': 2
}


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), unique=True)
    pass_hash = db.Column(db.String(32))
    role = db.Column(db.Integer, default=0)
    is_authenticated = True
    is_active = True

    def __init__(self, username, password, role):
        self.username = username
        self.pass_hash = hash_password(password)
        self.role = role

    def verify_password(self, password):
        return hash_password(password) == self.pass_hash

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.username

    def generate_auth_token(self, expiration=86400):
        s = Serializer(cfg.AppConfig['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(cfg.AppConfig['SECRET_KEY'])

        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token

        user = User.query.get(data['id'])
        return user
