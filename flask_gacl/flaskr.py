# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~

    A microblog example application written as Flask tutorial with
    Flask and sqlite3.

    :copyright: (c) 2014 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

import os, json
from itertools import chain
from sqlite3 import dbapi2 as sqlite3
from sqlite3 import OperationalError
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
import gacl, gacl_api, gacl_app
from common import *

# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME=['user1','user2','user3'],
    PASSWORD='def'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        # init gacl


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def get_gacl_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'gacl_db'):
        g.gacl_db = SQLAlchemy(app)
    return g.gacl_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
    if hasattr(g, 'gacl_db'):
        g.gacl_db.close()


@app.route('/')
def show_entries():
    data = {}
    data['username'] = session.get('username', None)
    data['user_tags'] = set(session.get('tags',[])) 
    db = get_db()
    try:
        cur = db.execute('select * from entries order by id desc')
    except OperationalError:
        return redirect(url_for('debugging'))
    entries = [Entry(entry) for entry in cur.fetchall()]
    if not session.get('logged_in'):
        entries = filter(lambda x: not x.private is 1, entries)
    else:
        entries = filter(lambda x: x.tags.intersection(data['user_tags']), entries)
    data['entries'] = entries
    return render_template('show_entries.html', **data)

@app.route('/requests')
@app.route('/requests/<status>')
def show_requests(status=None):
    data = {}
    username = session.get('username', None)
    usertags = set(session.get('tags',[]))
    data['username'] = username
    data['user_tags'] = usertags 
    db = get_db()
    try:
        cur = db.execute('select * from requests order by id desc')
    except OperationalError:
        return redirect(url_for('debugging'))
    entries = [Request(entry) for entry in cur.fetchall()]
    data['entries'] = filter(lambda x: x.tag in data['user_tags'], entries)
    return render_template('show_requests.html', **data)


@app.route('/channel/<channel>')
def show_channel(channel):
    data = {}
    data['username'] = session.get('username', None)
    data['user_tags'] = set(session.get('tags',[])) 
    db = get_db()
    try:
        cur = db.execute('select * from entries order by id desc')
    except OperationalError:
        return redirect(url_for('debugging'))
    entries = [Entry(entry) for entry in cur.fetchall()]
    if not session.get('logged_in'):
        entries = filter(lambda x: not x.private is 1, entries)
    else:
        entries = filter(lambda x: x.tags.intersection(data['user_tags']), entries)
    data['entries'] = filter(lambda x: channel in x.tags, entries)
    data['authors'] = set(entry.author for entry in entries)
    data['channel'] = channel
    return render_template('show_channel.html', **data)


@app.route('/author/<author>')
def show_author(author):
    data = {}
    data['username'] = session.get('username', None)
    data['user_tags'] = set(session.get('tags',[])) 
    db = get_db()
    try:
        cur = db.execute('select * from entries order by id desc')
    except OperationalError:
        return redirect(url_for('debugging'))
    entries = [Entry(entry) for entry in cur.fetchall()]
    if not session.get('logged_in'):
        entries = filter(lambda x: not x.private is 1, entries)
    else:
        entries = filter(lambda x: x.tags.intersection(data['user_tags']), entries)
    data['entries'] = filter(lambda x: author == x.author, entries)
    data['author_tags'] = set()
    for entry in data['entries']:
        data['author_tags'].update(entry.tags)     
    data['author'] = author
    return render_template('show_author.html', **data)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    try:
        cur = db.execute('select * from entries order by id desc')
    except OperationalError:
        return redirect(url_for('debugging'))
    all_tags = set(chain(*[Entry(entry).tags for entry in cur.fetchall()]))
    print 'all >', all_tags
    private = 1 if request.form.get('private', 0) else 0
    author = session.get('username')
    author_tags = session['tags']
    print 'author <', author_tags
    tags = set(request.form.get('tags', '').split())
    print 'tags <', tags
    new_tags = tags.difference(author_tags)
    print 'new tags <', new_tags
    restricted_tags = new_tags.intersection(all_tags)
    print 'restricted tags <', restricted_tags
    for tag in restricted_tags:
        db.execute('insert into requests (tag, author, status) values (?, ?, ?)',[
                 tag,
                 author,
                 'active', 
        ])
    db.commit()
    allowed_tags = tags.difference(restricted_tags)
    print 'allowed tags <', allowed_tags
    author_tags.extend(allowed_tags)
    print 'author >', author_tags
    session['tags'] = list(author_tags)
    print 'session <', session['tags'] 
    db.execute('insert into entries (title, text, author, tags, pending, private) values (?, ?, ?, ?, ?, ?)',
                 [request.form['title'], 
                 request.form['text'], 
                 author, 
                 json.dumps(list(allowed_tags)), 
                 json.dumps(list(restricted_tags)), 
                 private])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


  

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        print request.form['username']
        if request.form['username'] not in app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['username'] = request.form['username']
            db = get_db()
            cur = db.execute('select * from entries order by id desc')
            entries = cur.fetchall()
            tags = set()
            for entry in entries:
                if entry['author'] == session['username']:
                    tags.update(json.loads(entry['tags']))
            session['tags'] = list(tags)
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('tags', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


@app.route('/init')
def init():
    init_db()
    return redirect(url_for('show_entries'))


@app.route('/debugging')
def debugging():
    return render_template('debugging.html')


if __name__ == '__main__':
    app.run()
