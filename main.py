# Imports:
from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
# from os import urandom
from os import path, mkdir
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, TextAreaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired, Length, EqualTo
from helpers import loggedIn, randId, logoutUser, split_skills
from bcrypt import hashpw, gensalt


# Configurations:
APP_ROOT = path.dirname(path.abspath(__file__)) # app root = projects path
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/vasilis/pycourses.db' # sqlite db url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '\xc9!Zi\xab\x8b\xae}D`\x17\xc69\x81\xcd\x93\xec+\xf1\xf2s&DG'
app.jinja_env.filters['split_skills'] = split_skills # add custom filter in jinja-2
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB maximum bytes
# app.config['SECRET_KEY'] = urandom(24) # urandom() generates a 32 length random secret key
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

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(50), unique=False, nullable=False)
    surname = db.Column(db.String(50), unique=False, nullable=False)
    description = db.Column(db.String(1500), unique=False, nullable=False)
    avatar = db.Column(db.String(500), unique=False, nullable=False)
    skills = db.Column(db.String(1500), unique=False, nullable=False)

    def __init__(self, user_id, name, surname, avatar, description, skills):
        self.user_id = user_id
        self.name = name
        self.surname = surname
        self.avatar = avatar
        self.description = description
        self.skills = skills
    def __repr__(self):
        return '< Profile: '+self.user_id+' >'

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String(500), unique=False, nullable=False)
    description = db.Column(db.String(1500), unique=False, nullable=False)
    thumbnail = db.Column(db.String(500), unique=False, nullable=False)
    required_skills = db.Column(db.String(1500), unique=False, nullable=False)
    avg_rating = db.Column(db.Integer, unique=False, nullable=True)
    ratings = db.Column(db.Integer, unique=False, nullable=True)
    enrolled = db.Column(db.Integer, unique=False, nullable=True)

    def __init__(self, user_id, title, description, thumbnail, required_skills, avg_rating=0, ratings=0, enrolled=0):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.thumbnail = thumbnail
        self.required_skills = required_skills
        self.avg_rating = avg_rating
        self.ratings = ratings
        self.enrolled = enrolled
    def __repr__(self):
        return '< Course: '+self.user_id+' >'

# class Review(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, unique=True, nullable=False)
#     course_id = db.Column(db.Integer, unique=True, nullable=False)
#     text = db.Column(db.String(1500), unique=False, nullable=False)
#     stars = db.Column(db.Integer, unique=False, nullable=False)
#
#     def __init__(self, user_id, course_id, text, stars):
#         self.user_id = user_id
#         self.course_id = course_id
#         self.text = text
#         self.stars = stars
    #  def __repr__(self):
    #      return '< Review: '+self.user_id+' >'

# class Lesson(db.Model):
#     ...
#     def __init__(self, user_id, course_id, video, title, description, thumbnail):
#         self.user_id = user_id
#         self.course_id = course_id
#         self.description = description
#         self.thumbnail = thumbnail
#         self.video = video
#         self.title = title


# Forms:
class LoginForm(FlaskForm):
    username = TextField('Username', validators=[InputRequired('username is required !'), Length(min=10, max=25, message='username must be between 10 and 25 characters long !')])
    password = PasswordField('Password', validators=[InputRequired('password is required !'), Length(min=8, max=12, message='password must be between 8 and 12 characters long !')])

class RegisterForm(FlaskForm):
    username = TextField('Username', validators=[InputRequired('username is required !'), Length(min=10, max=25, message='username must be between 10 and 25 characters long !')])
    password = PasswordField('Password', validators=[InputRequired('password is required !'), Length(min=8, max=12, message='password must be between 8 and 12 characters long !'), EqualTo('confirm', message='passwords must match !')])
    confirm = PasswordField('Repeat Password')

class EditProfileForm(FlaskForm):
    name = TextField('Name', validators=[InputRequired('name is required !'), Length(min=4, max=50, message='name must be between 4 and 50 characters long !')])
    surname = TextField('Surname', validators=[InputRequired('surname is required !'), Length(min=4, max=50, message='surname must be between 4 and 50 characters long !')])
    avatar = FileField('Avatar', validators=[FileRequired(message='avatar is required !'), FileAllowed(['jpg'], 'images only!')])
    description = TextAreaField('Description', validators=[InputRequired('description is required !'), Length(min=10, max=1500, message='description must be between 10 and 1500 characters long !')])
    skills = TextAreaField('Skills', validators=[InputRequired('skills field is required !'), Length(min=2, max=1500, message='skills field must be between 2 and 1500 characters long !')])

class CourseForm(FlaskForm):
    title = TextField('Title', validators=[InputRequired('title is required !'), Length(min=4, max=50, message='name must be between 5 and 500 characters long !')])
    thumbnail = FileField('Thumbnail', validators=[FileRequired(message='thumbnail is required !'), FileAllowed(['jpg'], 'images only!')])
    description = TextAreaField('Description', validators=[InputRequired('description field is required !'), Length(min=10, max=1500, message='description must be between 10 and 1500 characters long !')])
    required_skills  = TextAreaField('Required skills', validators=[InputRequired('required skills are required !'), Length(min=2, max=1500, message='required skills must be between 2 and 1500 characters long !')])


# Views:
@app.route('/', methods=['GET'])
def home():
   username = loggedIn(session, LoggedIn)
   if username == False:
       form = LoginForm()
       return render_template('login.html', form=form)
   else:
       return render_template('index.html', username=username)

@app.route('/my-courses', methods=['GET'])
def my_courses():
    username = loggedIn(session, LoggedIn)
    if username == False:
        form = LoginForm()
        return render_template('login.html', form=form)

    user = User.query.filter_by(username=username).first()
    courses = Course.query.filter_by(user_id=user.id).all()
    return render_template('my_courses.html', username=username, courses=courses)

@app.route('/new-course', methods=['GET', 'POST'])
def course():
    username = loggedIn(session, LoggedIn)
    if username == False:
        form = LoginForm()
        return render_template('login.html', form=form)

    form = CourseForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()

        # save thumbnail
        thumbnail = form.thumbnail.data
        filename = secure_filename(thumbnail.filename)
        filename = ''+str(user.id)+'_'+'course'+'.jpg'
        target = path.join(APP_ROOT, 'static/courses/')
        if not path.isdir(target):
            mkdir(target)
        thumbnail.save(path.join(target, filename))

        # save course
        title = request.form['title']
        description = request.form['description']
        required_skills = request.form['required_skills']
        course = Course(user_id=user.id, title=title, description=description, thumbnail=filename, required_skills=required_skills)
        db.session.add(course)
        db.session.commit()

        return render_template('index.html', username=username)

    return render_template('new_course.html', form=form)

@app.route('/update-profile', methods=['GET', 'POST'])
def update_profile():
    username = loggedIn(session, LoggedIn)
    if username == False:
        form = LoginForm()
        return render_template('login.html', form=form)

    form = EditProfileForm()
    if form.validate_on_submit():
        # find user by username and his/her profile by his/her id
        user = User.query.filter_by(username=username).first()
        user_profile = Profile.query.filter_by(user_id=user.id).first()

        # update current user's profile data
        user_profile.name = request.form['name']
        user_profile.surname = request.form['surname']
        user_profile.description = request.form['description']
        user_profile.skills = request.form['skills']

        # update avatar
        avatar = form.avatar.data
        filename = secure_filename(avatar.filename) # maybe it's optional because i change the filename
        filename = ''+str(user.id)+'_'+'avatar'+'.jpg' # user-id_avatar.jpg
        target = path.join(APP_ROOT, 'static/avatars/') # target = project's path + /static/avatars
        if not path.isdir(target): # if target doesn't exist
            mkdir(target) # we create the target
        avatar.save(path.join(target, filename)) # save the file in the target
        user_profile.avatar = filename

        # save changes in profile table
        db.session.commit()
        return render_template('profile.html', username=username, user_profile=user_profile)

    return render_template('edit_profile.html', form=form)

@app.route('/profile', methods=['GET'])
def profile():
    username = loggedIn(session, LoggedIn)
    if username == False:
        form = LoginForm()
        return render_template('login.html', form=form)

    user = User.query.filter_by(username=username).first()
    user_profile = Profile.query.filter_by(user_id=user.id).first()
    user_skills = user_profile.skills.split(',')
    return render_template('profile.html', username=username, user_profile=user_profile, user_skills=user_skills)

@app.route('/register', methods=['GET', 'POST'])
def register():
    username = loggedIn(session, LoggedIn)
    if username != False:
        return render_template('index.html', username=username)

    form = RegisterForm()
    if form.validate_on_submit():
        hashedPwd = hashpw(str(request.form['password']).encode('utf-8'), gensalt()) # encrypt user's password
        user = User(username=request.form['username'], password=hashedPwd) # create user
        db.session.add(user)
        db.session.commit() # save new user in User table

        new_user = User.query.filter_by(username=request.form['username']).first() # new profile
        user_profile = Profile(user_id=new_user.id, name="no-name", surname="no-surname", avatar="saitama-batman.jpg", description="no-description", skills="no-skills")
        db.session.add(user_profile)
        db.session.commit() # save new profile in Profile table

        return render_template('registration_success.html', username=request.form['username'])
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = loggedIn(session, LoggedIn)
    if username != False:
        return render_template('index.html', username=username)

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

        rand_ID = str(randId())
        while True:
            user = LoggedIn.query.filter_by(rand_id=rand_ID).first()
            if user:
                rand_ID = randId()
            else:
                break

        userLoggedIn = LoggedIn(username=request.form['username'], rand_id=rand_ID)
        db.session.add(userLoggedIn)
        db.session.commit()
        session['user'] = rand_ID
        return render_template('index.html', username=userLoggedIn.username)
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    if not 'user' in session:
        form = LoginForm()
        return render_template('login.html', form=form)

    logoutUser(session=session, LoggedIn=LoggedIn, db=db)
    form = LoginForm()
    return render_template('login.html', form=form)


# Database and server set up:
if __name__ == '__main__':
   db.create_all()
   app.run(debug=True)
