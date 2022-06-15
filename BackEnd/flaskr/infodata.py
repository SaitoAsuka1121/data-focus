import sqlite3

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from sqlalchemy.exc import ArgumentError, OperationalError
from werkzeug.exceptions import abort
from flask import jsonify
from .auth import login_required
from .db import get_config_db
from .db import get_info_db
import json
from sqlalchemy import create_engine

bp = Blueprint('data', __name__, url_prefix='/data')


@bp.route("/headers", methods=['POST'])
@login_required
def get_headers():
    data = dict()
    data['column_names'] = list()
    uri = request.json['uri']
    name = request.json['name']
    if uri == 'local':
        db = get_info_db()
        result = db.execute(
            "PRAGMA table_info(" + name + ")"
        ).fetchall()
        for row in result:
            data['column_names'].append(row[1])
    else:
        engine = create_engine(uri)
        result = engine.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_schema='public' AND table_name= %s ;", name
        ).fetchall()
        for row in result:
            data['column_names'].append(row[0])
    return jsonify(data)


# TODO: 多表查询
# TODO: 聚集函数
# TODO: 动态SQL
@bp.route("/query", methods=['POST'])
@login_required
def query():
    data = dict()
    uri = request.json['uri']
    name = request.json['name']
    columns = request.json['columns']
    data['result'] = dict()
    group = request.json['group_by']
    result = ""
    type = request.json['chartstype']
    try:
        search_query = "SELECT {} FROM {}".format(columns, name)
        if group != "null":
            search_query = search_query + " GROUP BY {}".format(group)
        print(search_query)
        if uri == 'local':
            db = get_info_db()
            result = db.execute(
                search_query
            ).fetchall()
        else:
            engine = create_engine(uri)
            result = engine.execute(
                search_query
            ).fetchall()
    except sqlite3.OperationalError:
        data['error'] = "Wrong columns name!"
    cols = columns.split(',')
    if type == 'scatter':
        data['result'] = list()
        for row in result:
            t = list()
            for c in cols:
                t.append(dict(row)[c])
            data['result'].append(t)
    elif type == 'pie':
        data['result'] = list()
        for row in result:
            t = dict()
            if cols[0] == group:
                t['name'] = row[0]
                t['value'] = row[1]
            else:
                t['value'] = row[0]
                t['name'] = row[1]
            data['result'].append(t)
    else:
        for c in cols:
            data['result'][c] = list()
        for row in result:
            for c in cols:
                data['result'][c].append(dict(row)[c])
    return jsonify(data)
