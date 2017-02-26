from flask import request, jsonify, g
from flask_httpauth import HTTPBasicAuth

from app import app, cfg
from models import User, USER_ROLES, find_user_role
from managers import user_manager as um

auth = HTTPBasicAuth()


@app.route('/')
def index():
    return cfg.AppConfig['INDEX_GREETING']


@app.route('/api/v1/user', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')

    c = check_user_fields(username, password)
    if c is not None:
        return c

    user = um.new_user(username, password)

    return jsonify({
        'id': user.id,
        'username': user.username,
        'role': USER_ROLES[find_user_role(user.role)]
    }), 201


@app.route('/api/v1/user/<int:user_id>', methods=['GET'])
@auth.login_required
def get_user(user_id):
    user = um.get_user(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'role': USER_ROLES[find_user_role(user.role)]
    }), 200


@app.route('/api/v1/token')
@auth.login_required
def get_auth_token():
    token = um.get_auth_token(g.user)
    return jsonify({
        'id': g.user.id,
        'username': g.user.username,
        'role': g.user.role,
        'token': token.decode('ascii')
    }), 200


@app.route('/api/v1/user/<int:user_id>', methods=['POST'])
@auth.login_required
def update_role(user_id):
    c = check_role(g.user, [USER_ROLES['admin']])
    if c is not None:
        return c

    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return send_error('User with this ID is not found', 400)

    user = um.update_user_role(user, request.json.get('role'))
    return jsonify({
        'id': user.id,
        'username': user.username,
        'role': USER_ROLES[find_user_role(user.role)]
    }), 200


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)

    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False

    g.user = user
    return True


@app.route('/api/v1/neural/sample/add', methods=['POST'])
@auth.login_required
def neural_add_sample():
    # TODO: implement
    return send_error('(-_-)', 200)


@app.route('/api/v1/neural/recognize', methods=['POST'])
@auth.login_required
def neural_recognize():
    # TODO: implement
    return send_error('(-_-)', 200)


def check_user_fields(username, password):
    missing = []
    if username is None:
        missing.append('username')
    if password is None:
        missing.append('password')

    if len(missing) > 0:
        return send_error('Missing arguments', 400, args=missing)

    if User.query.filter_by(username=username).first() is not None:
        return send_error('User with the same name is already exists', 400)

    return None


def check_role(user, available_roles):
    if user.role not in available_roles:
        return send_error('You have not enough permissions', 400)


def send_error(message, status_code, args=None, description=None):
    return jsonify({
        'error': message,
        'args': args,
        'description': description
    }), status_code
