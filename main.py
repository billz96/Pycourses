# Imports:
from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import urandom
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo
from helpers import loggedIn, randId, logoutUser
from bcrypt import hashpw, gensalt


# Configuratios:
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/vasilis/pycourses.db' # sqlite db url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = urandom(24) # generate a random secret key
db = SQLAlchemy(app)


# Models:
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique = True, nullable=False)
    password = db.Column(db.String(32), nullable=False) # hashed password

    def __init__(self, username, password):
        self.username = username
        self.password = password
    def __repr__(self):
        return '< User: '+self.username+' >'

class LoggedIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique = True, nullable=False)
    rand_id = db.Column(db.String(32), unique = True, nullable=False)
    def __init__(self, username, rand_id):
        self.username = username
        self.rand_id = rand_id
    def __repr__(self):
        return '< LoggedInUser: '+self.username+' >'


# Forms:
class LoginForm(FlaskForm):
    username = TextField('Username', validators=[InputRequired('username is required !'), Length(min=10, max=25, message='username must be between 10 and 25 characters long !')])
    password = PasswordField('Password', validators=[InputRequired('password is required !'), Length(min=8, max=12, message='password must be between 8 and 12 characters long !')])

class RegisterForm(FlaskForm):
    username = TextField('Username', validators=[InputRequired('username is required !'), Length(min=10, max=25, message='username must be between 10 and 25 characters long !')])
    password = PasswordField('Password', validators=[InputRequired('password is required !'), Length(min=8, max=12, message='password must be between 8 and 12 characters long !'), EqualTo('confirm', message='Passwords must match !')])
    confirm = PasswordField('Repeat Password')


# Views:
@app.route('/home', methods=['GET'])
def home():
   username = loggedIn(session, LoggedIn)
   if username == False:
       form = LoginForm()
       return render_template('login.html', form=form)
   return render_template('index.html', username=username)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashedPwd = hashpw(str(request.form['password']).encode('utf-8'), gensalt()) # encrypt user's password
        user = User(username=request.form['username'], password=hashedPwd) # create user
        db.session.add(user)
        db.session.commit() # save new user in User table
        return render_template('registration_success.html', username=request.form['username'])
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        pwd = request.form['password']
        existing_user = User.query.filter_by(username=request.form['username']).first()
        if not existing_user:
            error = 'Username or password are incorrect.'
            return render_template('login.html', form=form, loggedInError=error)

        hash1 = hashpw(str(pwd).encode('utf-8'), str(existing_user.password).encode('utf-8'))
        hash2 = existing_user.password
        if hash1 != hash2:
            error = 'Username or password are incorrect.'
            return render_template('login.html', form=form, loggedInError=error)

        rand_ID = randId()
        while True:
            user = LoggedIn.query.filter_by(rand_id=rand_ID).first()
            if user:
                rand_ID = randId()
            else:
                break

        userLoggedIn = LoggedIn(username=request.form['username'], rand_id=rand_ID)
        session['user'] = rand_ID
        return render_template('index.html', username=userLoggedIn.username)
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    if loggedIn(session, LoggedIn) == False:
        form = LoginForm()
        return render_template('login.html', form=form)
    logoutUser(session=session, LoggedIn=LoggedIn, db=db)
    form = LoginForm()
    return render_template('login.html', form=form)


# Database and server set up:
if __name__ == '__main__':
   db.create_all()
   app.run(debug=True)
