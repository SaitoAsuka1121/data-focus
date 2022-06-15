from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from sqlalchemy.exc import ArgumentError, OperationalError
from werkzeug.exceptions import abort
import pandas
from flask import jsonify
from .auth import login_required
from .db import get_config_db
from .db import get_info_db
import json
from sqlalchemy import create_engine

bp = Blueprint('database', __name__, url_prefix='/database')


# def get_config_db():
#     if 'db' not in g:
#
#         g.db = sqlite3.connect(
#             current_app.config['DATABASE'],
#             detect_types=sqlite3.PARSE_DECLTYPES
#         )
#         g.db.row_factory = sqlite3.Row
#     return g.db


@bp.route('/list', methods=['GET'])
@login_required
def list_database():
    db = get_config_db()
    data = dict()
    data['database_list'] = list()
    result = db.execute(
        'SELECT * FROM databases;'
    ).fetchall()
    for item in result:
        data['database_list'].append(dict(item))
    return json.dumps(data)


@bp.route('/add', methods=['POST'])
@login_required
def add_database():
    data = dict()
    data['code'] = 0
    db = get_config_db()
    display_name = request.json['display_name']
    sqlalchemy_uri = request.json['sqlalchemy_uri']
    user_id = session.get('user_id')
    owner = db.execute(
        'SELECT username FROM user WHERE id = ?;', (user_id,)
    ).fetchone()[0]
    db.execute(
        'INSERT INTO databases values(?, ?, ?);', (display_name, sqlalchemy_uri, owner,)
    )
    db.commit()
    return jsonify(data)


@bp.route('/remove', methods=['POST'])
@login_required
def remove_database():
    data = dict()
    data['code'] = 0
    db = get_config_db()
    display_name = request.json['display_name']
    sqlalchemy_uri = request.json['source']
    db.execute(
        'DELETE FROM databases WHERE display_name = ? AND sqlalchemy_uri = ?;', (display_name, sqlalchemy_uri,)
    )
    db.commit()
    return jsonify(data)


@bp.route('/test', methods=['POST'])
@login_required
def test_connection():
    data = dict()
    data['code'] = 0
    uri = request.json['sqlalchemy_uri']
    try:
        engine = create_engine(uri)
        engine.connect()
    except ArgumentError:
        data['code'] = 1
        data['message'] = 'URI format error'
    except OperationalError:
        data['code'] = 1
        data['message'] = "can't connect to the database"
    except ValueError:
        data['code'] = 1
        data['message'] = "URI ERROR"
    return jsonify(data)


@bp.route('/get_tables', methods=['POST'])
@login_required
def get_tables():
    data = dict()
    data['code'] = 0
    uri = request.json['sqlalchemy_uri']
    table_list = list()
    try:
        if uri == 'local':
            db = get_info_db()
            result = db.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table';"
            ).fetchall()
            table_list = list()
            for row in result:
                item = dict()
                item['display_name'] = dict(row)['name']
                table_list.append(item)
            data['table_list'] = table_list
        else:
            engine = create_engine(uri)
            result = engine.execute(
                "SELECT tablename FROM pg_tables WHERE schemaname = 'public';"
            ).fetchall()
            for row in result:
                item = dict()
                item['display_name'] = row[0]
                table_list.append(item)
            data['table_list'] = table_list
    except ArgumentError:
        data['code'] = 1
        data['message'] = 'URI format error'
    except OperationalError:
        data['code'] = 1
        data['message'] = "can't connect to the database"
    return jsonify(data)


@bp.route('/tables', methods=['GET'])
@login_required
def tables():
    data = dict()
    data['code'] = 0
    db = get_config_db()
    data['table_list'] = list()
    result = db.execute(
        "SELECT * FROM tables;"
    )
    for item in result:
        data['table_list'].append(dict(item))
    return jsonify(data)


@bp.route('/add_table', methods=['POST'])
@login_required
def add_table():
    data = dict()
    data['code'] = 0
    db = get_config_db()
    name = request.json['name']
    source = request.json['source']
    table_name = request.json['databaseTablename']
    db.execute(
        "INSERT INTO tables values(?, ?, ?)", (name, source, table_name)
    )
    db.commit()
    return jsonify(data)


@bp.route('/remove_table', methods=['POST'])
@login_required
def remove_table():
    data = dict()
    data['code'] = 0
    db = get_config_db()
    name = request.json['display_name']
    source = request.json['source']
    table_name = request.json['databaseTablename']
    db.execute(
        "DELETE FROM tables where display_name = ? AND source = ? AND table_name = ?;", (name, source, table_name)
    )
    db.commit()
    return jsonify(data)


@bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    data = dict()
    data['code'] = 0
    uri = request.form['sqlalchemy_uri']
    name = request.form['display_name']
    filename = request.form['fileName']
    if filename.endswith('.csv'):
        f = request.files['excelFile']
        f = pandas.read_csv(f)
    elif filename.endswith('xlsx'):
        f = request.files['excelFile']
        f = pandas.read_excel(f)
    else:
        data['code'] = 1
        data['message'] = "文件类型暂不支持"
        return jsonify(data)
    if uri == 'local':
        engine = get_info_db()
    else:
        engine = create_engine(uri)
    f.to_sql(name, engine, index=False)
    return jsonify(data)
