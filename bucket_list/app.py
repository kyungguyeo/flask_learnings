from flask import Flask, render_template, json, request, redirect, url_for, flash, session as flask_session
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import create_engine
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
            return redirect('showProfile?firstname=' + _firstname)
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
                return redirect('showProfile')
    return render_template('signin.html', error = error)

@app.route('/showSignOut')
def signOut():
    if 'username' not in flask_session:
        return redirect(url_for('signIn'))
    else:
        flask_session.pop('user_id', None)
        return redirect(url_for('main'))

@app.route('/showProfile', methods=['POST','GET'])
def Profile():
    if 'username' not in flask_session:
        return redirect(url_for('main'))
    else:
        if request.method=='POST':
            this_user = session.query(Users).filter(Users.id == flask_session['user_id'])
            _task_decr = request.form['task_desc']
            _user_id = this_user.id
            _datecreated = datetime.now().time()
            new_task = Tasks(user_id=_user_id, task_description=_task_decr, date_created=_datecreated, completed = False, user=this_user)
            session.add(new_task)
            session.commit()
        elif request.method=='GET':
            all_tasks = session.query(Tasks).filter(Tasks.user_id == flask_session['user_id'])


        return render_template('profile.html')

if __name__ == "__main__":
    app.run(port=5002)
