import json
from json import JSONDecodeError

import requests
from flask import render_template, request, redirect, url_for, session, flash

from ui import app, cfg
from ui.forms import LoginForm, RegisterForm, UploadSampleForm, UploadToRecognizeForm
from ui.models import User, LoggedUser

api_url = cfg.ServerConfig['API_URL']
headers = cfg.ServerConfig['HEADERS']


@app.errorhandler(404)
def error_404(error):
    return _render_template('error_page.html', status_code=404, message='Page not found')


@app.errorhandler(401)
def error_401(error):
    return _render_template('error_page.html', status_code=401, message='Unauthorized access')


@app.errorhandler(400)
def error_400(error):
    return _render_template('error_page.html', status_code=400, message='Bad request')


@app.route('/')
def index():
    return recognize()


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if request.method == 'POST':

        if not form.validate_on_submit():
            flash('Wrong username or password', 'danger')
            return _render_template('login.html', form=form)

        r = requests.get(api_url + '/token',
                         headers=headers,
                         auth=(form.username.data, form.password.data))

        # Successful authorization
        if r.status_code == 200:
            data = json.loads(r.text)
            session['user'] = User(id=data['id'],
                                   username=data['username'],
                                   role=data['role'],
                                   token=data['token']).__dict__
            return redirect(url_for('recognize'))

        if r.status_code == 401:
            flash('Wrong username or password', 'danger')
            return _render_template('login.html', form=form)

        return _render_error(r)

    return _render_template('login.html', form=form)


@app.route('/logout')
def logout():
    if session['user']:
        del session['user']

    return redirect(url_for('index'))


@app.route('/join', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if request.method == 'POST':

        if not form.validate_on_submit():
            flash('Invalid name or/and password', 'danger')
            return _render_template('join.html', form=form)

        r = requests.post(api_url + '/user',
                          headers=headers,
                          data=json.dumps({'username': form.username.data,
                                           'password': form.password.data}))

        # Successful registration
        if r.status_code == 201:
            r = requests.get(api_url + '/token',
                             headers=headers,
                             auth=(form.username.data, form.password.data))
            data = json.loads(r.text)
            session['user'] = User(id=data['id'],
                                   username=data['username'],
                                   role=data['role'],
                                   token=data['token']).__dict__
            return redirect(url_for('recognize'))

        return _render_error(r)

    return _render_template('join.html', form=form)


@app.route('/recognize', methods=['POST', 'GET'])
def recognize():
    form = UploadToRecognizeForm()

    if request.method == 'POST':

        if not form.validate_on_submit():
            image_errors = form.image.errors
            for error in image_errors:
                flash(error, 'danger')
            return _render_template('index.html', form=form)

        file = form.image.data
        files = {file.name: (file.filename, file)}
        # TODO requests.exceptions.ConnectionError throws
        r = requests.post(api_url + '/neural/recognize',
                          headers=headers,
                          auth=(session['user']['token'], 'unused'),
                          files=files)

        # Successful upload
        if r.status_code == 200:
            flash('Your image has been successfully uploaded', 'info')
            return _render_template('index.html', form=form)

        return _render_error(r)

    return _render_template('index.html', form=form)


@app.route('/sample/add', methods=['POST', 'GET'])
def add_sample():
    form = UploadSampleForm()

    if request.method == 'POST':

        if not form.validate_on_submit():
            archived_images_errors = form.archived_images.errors
            for error in archived_images_errors:
                flash(error, 'danger')
            return _render_template('sample_add.html', form=form)

        file = form.archived_images.data
        files = {file.name: (file.filename, file)}
        r = requests.post(api_url + '/neural/sample/add',
                          headers=headers,
                          auth=(session['user']['token'], 'unused'),
                          files=files)

        # Successful upload
        if r.status_code == 200:
            flash('Your sample has been successfully uploaded', 'info')
            return _render_template('sample_add.html', form=form)

        return _render_error(r)

    return _render_template('sample_add.html', form=form)


def get_username(user_id):
    r = requests.get(api_url + '/user/' + str(user_id),
                     headers=headers,
                     auth=(session['user']['token'], 'unused'))
    if r.status_code == 200:
        return json.loads(r.text)['username']
    return None


def _render_template(template, **kwargs):
    return render_template(template,
                           user=(LoggedUser(username=session['user']['username'],
                                            role=session['user']['role'])
                                 if 'user' in session.keys() else None), **kwargs)


def _render_error(r):
    status = r.status_code
    try:
        text = json.loads(r.text)['error']
    except JSONDecodeError:
        text = r.text

    return _render_template('error_page.html', status_code=status, message=text)
