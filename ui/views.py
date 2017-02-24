import json

import requests
from flask import render_template, request, redirect, url_for, session, flash

from ui import app, cfg
from ui.forms import LoginForm, RegisterForm
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
    return _render_template('index.html')


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
            print(data)
            session['user'] = User(id=data['id'],
                                   username=data['username'],
                                   role=data['role'],
                                   token=data['token']).__dict__
            return redirect(url_for('index'))

        if r.status_code == 401:
            flash('Wrong username or password', 'danger')
            return _render_template('login.html', form=form)

        flash(json.loads(r.text)['error'], 'danger')
        return _render_template('login.html', form=form)

    else:
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

        # Successfully registration
        if r.status_code == 201:
            r = requests.get(api_url + '/token',
                             headers=headers,
                             auth=(form.username.data, form.password.data))
            data = json.loads(r.text)
            session['user'] = User(id=data['id'],
                                   username=data['username'],
                                   role=data['role'],
                                   token=data['token']).__dict__
            return redirect(url_for('index'))

        # Errors
        flash(json.loads(r.text)['error'], 'danger')
        return _render_template('join.html', form=form)

    else:
        return _render_template('join.html', form=form)


def get_username(user_id):
    r = requests.get(api_url + '/user/' + str(user_id),
                     headers=headers,
                     auth=(session['user']['token'], 'unused'))
    if r.status_code == 200:
        return json.loads(r.text)['username']
    return None


def _render_template(template, **kwargs):
    return render_template(template,
                           user=(LoggedUser(username=session['user']['username'])
                                 if 'user' in session.keys() else None), **kwargs)
