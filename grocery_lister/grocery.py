# all the imports
import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing

# create the application
app = Flask(__name__)

# configuration
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

#initalized the db
def init_db():
    db = get_db()
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        print('Initialized the database.')

#Opens a new database connection if there is none yet for the current application context.
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.db = connect_db()
    return g.db

@app.teardown_appcontext
#Closes the database again at the end of the request.
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.db.close()

@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('Welcome to Grocery Lister!')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Seeya Later!')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()