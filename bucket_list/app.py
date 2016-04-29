from flask import Flask, render_template, json, request, redirect, url_for, flash, session as flask_session
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from models import Users, Base, Tasks

app = Flask(__name__)

#Debug Mode
app.config['DEBUG'] = True
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'BucketLister'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
engine = create_engine('mysql://root@localhost')
engine.execute("USE Bucketlister") # select new db
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()
#secret key
app.secret_key = 'ge\xf9\xc3H\x1d\tQ\xbf\xa7\xc8#\x06^+\xa3\x00\xe9z,mA\xf1\xeb\x91'

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp', methods=['POST','GET'])
def signUp():
    error = None
    if request.method == 'POST':
        _firstname = request.form['inputFirstName']
        _lastname = request.form['inputLastName']
        _username = request.form['inputUsername']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        _datecreated = datetime.now().time()
        _hashed_password = generate_password_hash(_password)
        if session.query(Users).filter(Users.username == _username).all():
            error = 'Invalid credentials/credentials already taken.'
        else:
            new_user = Users(first_name=_firstname, last_name=_lastname, email=_email, password=_hashed_password, username=_username)
            session.add(new_user)
            session.commit()
            flask_session['username'] = _username
            return redirect('showProfile/' + _username)
    return render_template('signup.html', error=error)      

@app.route('/showSignIn', methods=['POST','GET'])
def signIn():
    error = None
    if request.method == 'POST': 
        _username = request.form['inputUsername']
        _password = request.form['inputPassword']
        user = session.query(Users).filter(Users.username == _username).one()
        _user_id = user.id
        if user:
            _firstname = user.first_name
            if not check_password_hash(user.password, _password):
                error = 'Invalid username or password'
            else:
                flask_session['user_id'] = _user_id
                return redirect('showProfile/' + _username)
    return render_template('signin.html', error = error)

@app.route('/showSignOut')
def signOut():
    if 'user_id' not in flask_session:
        return redirect('showSignIn')
    else:
        flask_session.pop('user_id', None)
        return redirect('/')

@app.route('/showProfile/<username>', methods=['POST','GET'])
def Profile(username):
    error=None
    if 'user_id' not in flask_session:
        return redirect(url_for('main'))
    else:
        if request.method=='POST':
            this_user = session.query(Users).filter(Users.id == flask_session['user_id']).one()
            _task_desc = request.form['inputTask']
            _user_id = this_user.id
            _datecreated = datetime.utcnow()
            _first_name = this_user.first_name
            new_task = Tasks(user_id=_user_id, task_description=_task_desc, date_created=_datecreated, completed=False, user=this_user)
            session.add(new_task)
            session.commit()
            all_tasks = session.query(Tasks).filter(Tasks.user_id == flask_session['user_id'], Tasks.completed == False).all()
            return render_template('profile.html', name=_first_name, tasks=all_tasks, error=error)
        elif request.method=='GET':
            if session.query(Tasks).filter(Tasks.user_id == flask_session['user_id']).all():
                all_tasks = session.query(Tasks).filter(Tasks.user_id == flask_session['user_id'], Tasks.completed == False).all()
            else:
                all_tasks = []
            _first_name = session.query(Users).filter(Users.id == flask_session['user_id']).one().first_name
            return render_template('profile.html', name=_first_name, tasks=all_tasks, error=error)

@app.route('/deleteTask', methods=['POST','GET'])
def Delete():
    error = None
    if request.method=='POST':
        _task_id = request.form.get('task-id')
        _username = session.query(Users).filter(Users.id == flask_session['user_id']).one().username
        session.query(Tasks).filter(Tasks.id == _task_id).delete()
        session.commit()
        return redirect('showProfile/' + _username)

@app.route('/completeTask', methods=['POST','GET'])
def Complete():
    error = None
    if request.method=='POST':
        _task_id = request.form.get('task-id')
        _username = session.query(Users).filter(Users.id == flask_session['user_id']).one().username
        session.query(Tasks).filter(Tasks.id == _task_id).update({"completed": True})
        session.commit()
        return redirect('showProfile/' + _username)

if __name__ == "__main__":
    app.run(port=5002)
