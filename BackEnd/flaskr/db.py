import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_config_db():
    if 'config_db' not in g:
        g.config_db = sqlite3.connect(
            current_app.config['CONFIG_DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.config_db.row_factory = sqlite3.Row
    return g.config_db


def get_info_db():
    if 'info_db' not in g:
        g.info_db = sqlite3.connect(
            current_app.config['INFO_DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.info_db.row_factory = sqlite3.Row
    return g.info_db


def close_db(e=None):
    config_db = g.pop('config_db', None)
    if config_db is not None:
        config_db.close()


def init_db():
    config_db = get_config_db()
    with current_app.open_resource('init-sql\\schema.sql') as f:
        config_db.executescript(f.read().decode('utf8'))

    info_db = get_info_db()
    with current_app.open_resource('init-sql\\info.sql') as f:
        info_db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
