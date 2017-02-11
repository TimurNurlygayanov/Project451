from flask.ext.httpauth import HTTPBasicAuth

from app import app


auth = HTTPBasicAuth()


@app.route('/')
def index():
    return "Hello, world!"


@app.route('/api/user', methods=['POST'])
def new_user():
    # TODO: implement
    return None


@app.route('/api/user/<int:user_id>', methods=['GET'])
@auth.login_required
def get_user(user_id):
    # TODO: implement
    return None


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    # TODO: implement
    return None


@auth.verify_password
def verify_password(username_or_token, password):
    # TODO: implement
    return None


@app.route('/api/neural/learn')
@auth.login_required
def neural_learn():
    # TODO: implement
    return None


@app.route('/api/neural/recognize')
@auth.login_required
def neural_recognize():
    # TODO: implement
    return None
