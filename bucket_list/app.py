from flask import Flask, render_template, json, request, redirect, url_for, flash, session
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime

mysql = MySQL()
app = Flask(__name__)

#Debug Mode
app.config['DEBUG'] = True
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'johnnyyeo'
app.config['MYSQL_DATABASE_PASSWORD'] = 'abcd1234'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
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
        conn = mysql.connect()
        cursor = conn.cursor()
        _hashed_password = generate_password_hash(_password)
        cursor.callproc('sp_createUser',(_firstname, _lastname, _username, _email,_hashed_password))
        data = cursor.fetchall()
        len(data)
        if len(data) is 0:
            conn.commit()
            cursor.close() 
            conn.close()
            session['username'] = _username
            return redirect('showProfile?firstname=' + _firstname)
        else:
            error = 'Invalid credentials/credentials already taken.'
    return render_template('signup.html', error=error)      

@app.route('/showSignIn', methods=['POST','GET'])
def signIn():
    error = None
    if request.method == 'POST':                    
        _username = request.form['inputUsername']
        _password = request.form['inputPassword']
        conn = mysql.connect()
        cursor = conn.cursor()
        _hashed_password = generate_password_hash(_password)
        cursor.execute("""
            SELECT username, password, first_name, last_name 
            FROM users 
            WHERE username = %s""",
            (_username,))
        data = cursor.fetchall()
        if data:
            _firstname = data[0][2]
            if not check_password_hash(data[0][1], _password):
                error = 'Invalid username or password'
            else:
                session['username'] = _username
                return redirect('showProfile?firstname=' + _firstname)
        cursor.close()
        conn.close()
    return render_template('signin.html', error = error)

@app.route('/showSignOut')
def signOut():
    if 'username' not in session:
        return redirect(url_for('signIn'))
    else:
        session.pop('username', None)
        return redirect(url_for('main'))

@app.route('/showProfile')
def Profile():
    if 'username' not in session:
        return redirect(url_for('main'))
    else:
        return render_template('profile.html')

if __name__ == "__main__":
    app.run(port=5002)
