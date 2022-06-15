import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify,
)
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_config_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['POST'])
def register():
    data = dict()
    data['code'] = 0
    try:
        username = request.json['username']
        password = request.json['password']
        db = get_config_db()
        if db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            data['code'] = 1
            data['message'] = 'username already exist!'
    except KeyError:
        data['code'] = 1
        data['message'] = 'username or password is null'
    if data['code'] == 0:
        db.execute(
            'INSERT INTO user (username, password) VALUES (?, ?)',
            (username, generate_password_hash(password))
        )
        db.commit()
    return jsonify(data)


@bp.route('/login', methods=['POST'])
def login():
    data = dict()
    data['code'] = 0
    try:
        username = request.json['username']
        password = request.json['password']
        db = get_config_db()
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        if user is None or not check_password_hash(user['password'], password):
            data['code'] = 1
            data['message'] = 'username or password is incorrect'
    except KeyError:
        data['code'] = 1
        data['message'] = 'username or password is null'
    if data['code'] == 0:
        session.clear()
        session['user_id'] = user['id']
    return jsonify(data)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_config_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    data = dict()
    data['code'] = 0
    session.clear()
    return jsonify(data)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return "Please Login First"
        return view(**kwargs)
    return wrapped_view
