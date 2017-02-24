from app import db

from models import User, USER_ROLES


def get_user(user_id):
    return User.query.filter_by(id=user_id).first()


def new_user(username, password):
    user = User(username=username, password=password, role=USER_ROLES['user'])
    db.session.add(user)
    db.session.commit()

    return user


def get_auth_token(user):
    return user.generate_auth_token()


def update_user_role(user, new_role):
    role = USER_ROLES[new_role]
    User.query.filter_by(id=user.get_id()).update({'role': role})
    return User.query.filter_by(id=user.get_id()).first()

