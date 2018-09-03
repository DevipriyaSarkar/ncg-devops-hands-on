import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
import psycopg2


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if 'db' not in g:
        db_name = "dbname"
        db_user = "dbusername"
        db_password = "dbpassword"
        db_host = "10.0.2.2"
        db_port = "2332"

        conn = psycopg2.connect(database=db_name, user = db_user, password = db_password, host = db_host, port = db_port)
        g.db = conn.cursor()

    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.execute(f.read().decode('utf8'))

    print("Initialise db")


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
